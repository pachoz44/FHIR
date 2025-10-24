# -*- coding: utf-8 -*-
import json, uuid, re
from datetime import datetime

# ----------------- Configuración -----------------
# Usa tu dominio organizacional aquí:
BASE_NAMINGSYSTEM_URI = "http://hospital.local/fhir/NamingSystem/"

# ----------------- Utilidades -----------------
def split_segments(msg: str):
    return [l for l in re.split(r'\r\n|\n|\r', msg) if l.strip()]

def parse_msh(lines):
    msh = next(l for l in lines if l.startswith("MSH"))
    fs = msh[3]
    fields = msh.split(fs)
    enc = fields[1] if len(fields) > 1 else "^~\\&"
    return {"field": fs, "comp": enc[0] if len(enc) > 0 else "^"}

def seg_fields(seg, sep): return seg.split(sep)
def comp(val, cs): return val.split(cs) if val else []
def get_field(fields, idx): return fields[idx] if idx < len(fields) else ""

def parse_ts(ts: str):
    if not ts: return None
    m = re.match(r'^(\d{4})(\d{2})?(\d{2})?(\d{2})?(\d{2})?(\d{2})?', ts)
    if not m: return None
    y, mo, d, hh, mm, ss = m.groups()
    mo = mo or "01"; d = d or "01"; hh = hh or "00"; mm = mm or "00"; ss = ss or "00"
    try:
        return datetime(int(y), int(mo), int(d), int(hh), int(mm), int(ss)).isoformat() + "Z"
    except: return None

def parse_cwe(val, cs):
    c = comp(val, cs)
    code  = c[0] if len(c) > 0 else None
    text  = c[1] if len(c) > 1 else None
    sysid = c[2] if len(c) > 2 else None
    system = {
        "LN": "http://loinc.org",
        "L": "http://loinc.org",
        "SCT": "http://snomed.info/sct",
        "UCUM": "http://unitsofmeasure.org"
    }.get(sysid)
    return code, text, system

def parse_ucum(obx6, cs):
    code, text, sys = parse_cwe(obx6, cs)
    return code, text, sys or "http://unitsofmeasure.org"

def parse_ref_range(rr_str):
    if not rr_str: return None
    m = re.match(r'^\s*([\-]?\d+(\.\d+)?)\s*[-–]\s*([\-]?\d+(\.\d+)?).*$', rr_str)
    if m:
        return {"low": {"value": float(m.group(1))},
                "high": {"value": float(m.group(3))}}
    return {"text": rr_str}

def make_narrative(text): 
    return {"status": "generated",
            "div": f"<div xmlns='http://www.w3.org/1999/xhtml'>{text}</div>"}

def make_identifier(system_raw, value):
    # ✅ Ahora usa tu dominio organizacional
    if not system_raw:
        return {"system": BASE_NAMINGSYSTEM_URI + "local", "value": value}
    if not (system_raw.startswith("http://") or system_raw.startswith("https://")):
        system_raw = BASE_NAMINGSYSTEM_URI + system_raw
    return {"system": system_raw, "value": value}

OBS_STATUS_MAP = {"F": "final", "C": "corrected", "P": "preliminary"}
INTERP_ALLOWED = {"L","H","LL","HH","N","A","AA","<",">","POS","NEG"}

# ----------------- Conversión ORU → FHIR -----------------
def oru_to_fhir_bundle(hl7_message: str, as_transaction=False):
    segs = split_segments(hl7_message)
    seps = parse_msh(segs); FS, CS = seps["field"], seps["comp"]

    pid = None; groups = []; curr_obr = None
    for line in segs:
        f = seg_fields(line, FS); tag = f[0]
        if tag == "PID": pid = f
        elif tag == "OBR":
            curr_obr = {"obr": f, "obx": []}; groups.append(curr_obr)
        elif tag == "OBX" and curr_obr: curr_obr["obx"].append(f)

    # --- Patient ---
    patient_uuid = f"urn:uuid:{uuid.uuid4()}"
    patient = {"resourceType": "Patient", "text": make_narrative("Patient")}
    if pid:
        cx = comp(get_field(pid,3), CS)
        id_val = cx[0] if len(cx)>0 else None
        id_sys = cx[3] if len(cx)>3 else None
        if id_val:
            patient["identifier"]=[make_identifier(id_sys or "local", id_val)]
        xpn = comp(get_field(pid,5), CS)
        if xpn: patient["name"]=[{"family": xpn[0], "given": xpn[1:2]}]
        birth = parse_ts(get_field(pid,7))
        if birth: patient["birthDate"]=birth[:10]
        gmap={"M":"male","F":"female"}; patient["gender"]=gmap.get(get_field(pid,8),"unknown")
    entries=[{"fullUrl": patient_uuid, "resource": patient}]

    # --- Groups (OBR→DiagnosticReport, OBX→Observation) ---
    for grp in groups:
        obr, obxs = grp["obr"], grp["obx"]
        dr_uuid = f"urn:uuid:{uuid.uuid4()}"; result_refs=[]
        performer = []
        prov = comp(get_field(obr,16), CS)
        if prov: performer=[{"display": " ".join([p for p in prov if p])}]

        for obx in obxs:
            obx3, obx5, obx6 = get_field(obx,3), get_field(obx,5), get_field(obx,6)
            obx7, obx8, obx11, obx14 = get_field(obx,7), get_field(obx,8), get_field(obx,11), get_field(obx,14)
            code_c, code_txt, code_sys = parse_cwe(obx3, CS)
            obs_uuid=f"urn:uuid:{uuid.uuid4()}"
            obs={"resourceType":"Observation","text":make_narrative(f"Result {code_txt or code_c}"),
                 "status":OBS_STATUS_MAP.get(obx11,"final"),
                 "category":[{"coding":[{"system":"http://terminology.hl7.org/CodeSystem/observation-category","code":"laboratory"}]}],
                 "code":{"coding":[{"system":code_sys or "http://loinc.org","code":code_c}],
                         "text": code_txt or code_c},
                 "subject":{"reference":patient_uuid}}
            eff=parse_ts(obx14) or parse_ts(get_field(obr,7))
            if eff: obs["effectiveDateTime"]=eff
            if get_field(obx,2)=="NM":
                try: val=float(obx5)
                except: val=None
                if val is not None:
                    u_code,u_text,u_sys=parse_ucum(obx6,CS)
                    obs["valueQuantity"]={"value":val,"unit":u_text or u_code,
                                          "system":u_sys,"code":u_code or u_text}
            elif get_field(obx,2) in ("ST","TX"): obs["valueString"]=obx5
            rr=parse_ref_range(obx7)
            if rr: obs["referenceRange"]=[rr]
            if obx8 in INTERP_ALLOWED:
                obs["interpretation"]=[{"coding":[{"system":"http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation","code":obx8}]}]
            if performer: obs["performer"]=performer
            entries.append({"fullUrl":obs_uuid,"resource":obs}); result_refs.append({"reference":obs_uuid})

        dr={"resourceType":"DiagnosticReport","text":make_narrative("Lab report"),
            "status":"final","category":[{"coding":[{"system":"http://terminology.hl7.org/CodeSystem/v2-0074","code":"LAB"}]}],
            "code":{"coding":[{"system":"http://loinc.org","code":get_field(obr,4).split(CS)[0]}],
                    "text": get_field(obr,4).split(CS)[1] if CS in get_field(obr,4) else "Lab report"},
            "subject":{"reference":patient_uuid},
            "result":result_refs}
        eff=parse_ts(get_field(obr,7))
        if eff: dr["effectiveDateTime"]=eff
        if performer: dr["performer"]=performer
        entries.append({"fullUrl":dr_uuid,"resource":dr})

    return {"resourceType":"Bundle","type":"collection","entry":entries}

# ----------------- Ejemplo -----------------
if __name__=="__main__":
    hl7 = """MSH|^~\\&|LIS|LAB|EHR|HOSP|202508261030||ORU^R01|12345|P|2.5
PID|||123456^^^HOSP||GARCIA^JUAN||19800101|M
OBR|1||ORD448811|24323-8^Lab report^LN|||202508261200|||||||||1234^MEDICO^ANA||||||||F
OBX|1|NM|2345-7^Glucose^LN||105|mg/dL|70-110|H|||F|||202508261200
OBX|2|ST|718-7^Hemoglobin^LN||Normal|||N|||F|||202508261200
"""
    b=oru_to_fhir_bundle(hl7)
    print(json.dumps(b,indent=2,ensure_ascii=False))
