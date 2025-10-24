-- Tabla Patients
CREATE TABLE IF NOT EXISTS Patients (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    dob DATE,
    gender TEXT,
    address TEXT
);

-- Tabla Doctors
CREATE TABLE IF NOT EXISTS Doctors (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

-- Tabla Diagnoses (con SNOMED CT codes)
CREATE TABLE IF NOT EXISTS Diagnoses (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER,
    code TEXT,  -- SNOMED CT code
    description TEXT,
    date DATE,
    doctor_id INTEGER,
    FOREIGN KEY (patient_id) REFERENCES Patients(id),
    FOREIGN KEY (doctor_id) REFERENCES Doctors(id)
);

-- Tabla AllergyIntolerances (con SNOMED CT codes)
CREATE TABLE IF NOT EXISTS AllergyIntolerances (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER,
    code TEXT,  -- SNOMED CT code
    substance TEXT,
    reaction TEXT,
    severity TEXT,
    FOREIGN KEY (patient_id) REFERENCES Patients(id)
);

-- Tabla Medications (con SNOMED CT codes)
CREATE TABLE IF NOT EXISTS Medications (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER,
    code TEXT,  -- SNOMED CT code
    name TEXT,
    dosage TEXT,
    start_date DATE,
    doctor_id INTEGER,
    FOREIGN KEY (patient_id) REFERENCES Patients(id),
    FOREIGN KEY (doctor_id) REFERENCES Doctors(id)
);

-- Tabla Coverages
CREATE TABLE IF NOT EXISTS Coverages (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER,
    insurer TEXT,
    policy_number TEXT,
    start_date DATE,
    end_date DATE,
    FOREIGN KEY (patient_id) REFERENCES Patients(id)
);

-- Insertar Doctors
INSERT INTO Doctors (id, name) VALUES (1, 'Dr. Smith');
INSERT INTO Doctors (id, name) VALUES (2, 'Dr. Johnson');
INSERT INTO Doctors (id, name) VALUES (3, 'Dr. Williams');
INSERT INTO Doctors (id, name) VALUES (4, 'Dr. Brown');
INSERT INTO Doctors (id, name) VALUES (5, 'Dr. Jones');

-- Insertar Patients (mismos 25 ficticios)
INSERT INTO Patients (id, name, dob, gender, address) VALUES (1, 'Quinn Garcia', '1976-12-11', 'Other', '5087 Elm St, Phoenix, USA');
INSERT INTO Patients (id, name, dob, gender, address) VALUES (2, 'Katie Davis', '1990-11-06', 'Other', '8566 Pine St, Chicago, USA');
INSERT INTO Patients (id, name, dob, gender, address) VALUES (3, 'Jane Thomas', '1986-07-30', 'Female', '321 Cedar St, Houston, USA');
INSERT INTO Patients (id, name, dob, gender, address) VALUES (4, 'Quinn Hernandez', '1953-10-27', 'Male', '1125 Cedar St, Phoenix, USA');
INSERT INTO Patients (id, name, dob, gender, address) VALUES (5, 'Olivia Jackson', '1965-09-06', 'Female', '5834 Pine St, Chicago, USA');
INSERT INTO Patients (id, name, dob, gender, address) VALUES (6, 'Olivia Martin', '1986-09-09', 'Other', '2170 Elm St, Houston, USA');
INSERT INTO Patients (id, name, dob, gender, address) VALUES (7, 'Leo Anderson', '1989-06-24', 'Female', '1676 Main St, Chicago, USA');
INSERT INTO Patients (id, name, dob, gender, address) VALUES (8, 'Leo Rodriguez', '1988-02-14', 'Female', '5622 Main St, New York, USA');
INSERT INTO Patients (id, name, dob, gender, address) VALUES (9, 'Quinn Garcia', '1987-07-14', 'Male', '6310 Oak St, Phoenix, USA');
INSERT INTO Patients (id, name, dob, gender, address) VALUES (10, 'Eve Taylor', '1952-03-25', 'Female', '820 Elm St, Los Angeles, USA');
INSERT INTO Patients (id, name, dob, gender, address) VALUES (11, 'Sophia Martin', '1990-10-28', 'Female', '643 Cedar St, Los Angeles, USA');
INSERT INTO Patients (id, name, dob, gender, address) VALUES (12, 'Henry White', '1986-09-08', 'Female', '5119 Main St, Los Angeles, USA');
INSERT INTO Patients (id, name, dob, gender, address) VALUES (13, 'Mia Thomas', '1956-03-21', 'Male', '1523 Pine St, Houston, USA');
INSERT INTO Patients (id, name, dob, gender, address) VALUES (14, 'Ryan Smith', '1993-07-14', 'Other', '7384 Main St, Chicago, USA');
INSERT INTO Patients (id, name, dob, gender, address) VALUES (15, 'Grace Harris', '1977-12-22', 'Other', '3617 Pine St, Chicago, USA');
INSERT INTO Patients (id, name, dob, gender, address) VALUES (16, 'Noah Miller', '1994-08-19', 'Other', '9849 Oak St, Phoenix, USA');
INSERT INTO Patients (id, name, dob, gender, address) VALUES (17, 'Grace Rodriguez', '1995-08-16', 'Female', '895 Elm St, Los Angeles, USA');
INSERT INTO Patients (id, name, dob, gender, address) VALUES (18, 'Ryan Lee', '1999-07-10', 'Other', '3349 Pine St, Houston, USA');
INSERT INTO Patients (id, name, dob, gender, address) VALUES (19, 'Victor Rodriguez', '1981-05-14', 'Other', '5309 Pine St, Houston, USA');
INSERT INTO Patients (id, name, dob, gender, address) VALUES (20, 'Bob Jackson', '1975-02-26', 'Other', '3445 Oak St, Phoenix, USA');
INSERT INTO Patients (id, name, dob, gender, address) VALUES (21, 'Mia Smith', '1973-05-27', 'Other', '1264 Cedar St, New York, USA');
INSERT INTO Patients (id, name, dob, gender, address) VALUES (22, 'Eve Hernandez', '1997-12-23', 'Female', '809 Main St, Phoenix, USA');
INSERT INTO Patients (id, name, dob, gender, address) VALUES (23, 'Bob Anderson', '1968-03-07', 'Female', '9268 Main St, Phoenix, USA');
INSERT INTO Patients (id, name, dob, gender, address) VALUES (24, 'Katie Hernandez', '1976-02-26', 'Other', '7742 Pine St, New York, USA');
INSERT INTO Patients (id, name, dob, gender, address) VALUES (25, 'Jane Moore', '1967-01-03', 'Male', '8853 Main St, Los Angeles, USA');

-- Insertar Diagnoses (ejemplos SNOMED CT)
INSERT INTO Diagnoses (id, patient_id, code, description, date, doctor_id) VALUES (1, 1, '73211009', 'Diabetes mellitus', '2023-01-15', 1);
INSERT INTO Diagnoses (id, patient_id, code, description, date, doctor_id) VALUES (2, 2, '38341003', 'Hypertension', '2023-02-20', 2);
INSERT INTO Diagnoses (id, patient_id, code, description, date, doctor_id) VALUES (3, 3, '195967001', 'Asthma', '2023-03-10', 3);
INSERT INTO Diagnoses (id, patient_id, code, description, date, doctor_id) VALUES (4, 4, '233604007', 'Pneumonia', '2023-04-05', 4);
INSERT INTO Diagnoses (id, patient_id, code, description, date, doctor_id) VALUES (5, 5, '35489007', 'Depression', '2023-05-12', 5);
INSERT INTO Diagnoses (id, patient_id, code, description, date, doctor_id) VALUES (6, 6, '22298006', 'Myocardial infarction', '2023-06-18', 1);
INSERT INTO Diagnoses (id, patient_id, code, description, date, doctor_id) VALUES (7, 7, '271737000', 'Anemia', '2023-07-22', 2);
INSERT INTO Diagnoses (id, patient_id, code, description, date, doctor_id) VALUES (8, 8, '73211009', 'Diabetes mellitus', '2023-08-30', 3);
INSERT INTO Diagnoses (id, patient_id, code, description, date, doctor_id) VALUES (9, 9, '38341003', 'Hypertension', '2023-09-14', 4);
INSERT INTO Diagnoses (id, patient_id, code, description, date, doctor_id) VALUES (10, 10, '195967001', 'Asthma', '2023-10-25', 5);
INSERT INTO Diagnoses (id, patient_id, code, description, date, doctor_id) VALUES (11, 11, '233604007', 'Pneumonia', '2023-11-08', 1);
INSERT INTO Diagnoses (id, patient_id, code, description, date, doctor_id) VALUES (12, 12, '35489007', 'Depression', '2023-12-16', 2);
INSERT INTO Diagnoses (id, patient_id, code, description, date, doctor_id) VALUES (13, 13, '22298006', 'Myocardial infarction', '2024-01-19', 3);
INSERT INTO Diagnoses (id, patient_id, code, description, date, doctor_id) VALUES (14, 14, '271737000', 'Anemia', '2024-02-27', 4);
INSERT INTO Diagnoses (id, patient_id, code, description, date, doctor_id) VALUES (15, 15, '73211009', 'Diabetes mellitus', '2024-03-11', 5);
INSERT INTO Diagnoses (id, patient_id, code, description, date, doctor_id) VALUES (16, 16, '38341003', 'Hypertension', '2024-04-23', 1);
INSERT INTO Diagnoses (id, patient_id, code, description, date, doctor_id) VALUES (17, 17, '195967001', 'Asthma', '2024-05-09', 2);
INSERT INTO Diagnoses (id, patient_id, code, description, date, doctor_id) VALUES (18, 18, '233604007', 'Pneumonia', '2024-06-17', 3);
INSERT INTO Diagnoses (id, patient_id, code, description, date, doctor_id) VALUES (19, 19, '35489007', 'Depression', '2024-07-28', 4);
INSERT INTO Diagnoses (id, patient_id, code, description, date, doctor_id) VALUES (20, 20, '22298006', 'Myocardial infarction', '2024-08-04', 5);
INSERT INTO Diagnoses (id, patient_id, code, description, date, doctor_id) VALUES (21, 21, '271737000', 'Anemia', '2024-09-13', 1);
INSERT INTO Diagnoses (id, patient_id, code, description, date, doctor_id) VALUES (22, 22, '73211009', 'Diabetes mellitus', '2024-10-21', 2);
INSERT INTO Diagnoses (id, patient_id, code, description, date, doctor_id) VALUES (23, 23, '38341003', 'Hypertension', '2024-11-02', 3);
INSERT INTO Diagnoses (id, patient_id, code, description, date, doctor_id) VALUES (24, 24, '195967001', 'Asthma', '2024-12-15', 4);
INSERT INTO Diagnoses (id, patient_id, code, description, date, doctor_id) VALUES (25, 25, '233604007', 'Pneumonia', '2025-01-26', 5);

-- Insertar AllergyIntolerances (ejemplos SNOMED CT)
INSERT INTO AllergyIntolerances (id, patient_id, code, substance, reaction, severity) VALUES (1, 1, '91936005', 'Penicillin', 'Rash', 'Mild');
INSERT INTO AllergyIntolerances (id, patient_id, code, substance, reaction, severity) VALUES (2, 2, '91935009', 'Nuts', 'Anaphylaxis', 'Severe');
INSERT INTO AllergyIntolerances (id, patient_id, code, substance, reaction, severity) VALUES (3, 3, '213020009', 'Eggs', 'Hives', 'Moderate');
INSERT INTO AllergyIntolerances (id, patient_id, code, substance, reaction, severity) VALUES (4, 4, '300916003', 'Latex', 'Itching', 'Mild');
INSERT INTO AllergyIntolerances (id, patient_id, code, substance, reaction, severity) VALUES (5, 5, '416098002', 'Aspirin', 'Nausea', 'Moderate');
INSERT INTO AllergyIntolerances (id, patient_id, code, substance, reaction, severity) VALUES (6, 6, '91936005', 'Penicillin', 'Rash', 'Mild');
INSERT INTO AllergyIntolerances (id, patient_id, code, substance, reaction, severity) VALUES (7, 7, '91935009', 'Nuts', 'Anaphylaxis', 'Severe');
INSERT INTO AllergyIntolerances (id, patient_id, code, substance, reaction, severity) VALUES (8, 8, '213020009', 'Eggs', 'Hives', 'Moderate');
INSERT INTO AllergyIntolerances (id, patient_id, code, substance, reaction, severity) VALUES (9, 9, '300916003', 'Latex', 'Itching', 'Mild');
INSERT INTO AllergyIntolerances (id, patient_id, code, substance, reaction, severity) VALUES (10, 10, '416098002', 'Aspirin', 'Nausea', 'Moderate');
INSERT INTO AllergyIntolerances (id, patient_id, code, substance, reaction, severity) VALUES (11, 11, '91936005', 'Penicillin', 'Rash', 'Mild');
INSERT INTO AllergyIntolerances (id, patient_id, code, substance, reaction, severity) VALUES (12, 12, '91935009', 'Nuts', 'Anaphylaxis', 'Severe');
INSERT INTO AllergyIntolerances (id, patient_id, code, substance, reaction, severity) VALUES (13, 13, '213020009', 'Eggs', 'Hives', 'Moderate');
INSERT INTO AllergyIntolerances (id, patient_id, code, substance, reaction, severity) VALUES (14, 14, '300916003', 'Latex', 'Itching', 'Mild');
INSERT INTO AllergyIntolerances (id, patient_id, code, substance, reaction, severity) VALUES (15, 15, '416098002', 'Aspirin', 'Nausea', 'Moderate');
INSERT INTO AllergyIntolerances (id, patient_id, code, substance, reaction, severity) VALUES (16, 16, '91936005', 'Penicillin', 'Rash', 'Mild');
INSERT INTO AllergyIntolerances (id, patient_id, code, substance, reaction, severity) VALUES (17, 17, '91935009', 'Nuts', 'Anaphylaxis', 'Severe');
INSERT INTO AllergyIntolerances (id, patient_id, code, substance, reaction, severity) VALUES (18, 18, '213020009', 'Eggs', 'Hives', 'Moderate');
INSERT INTO AllergyIntolerances (id, patient_id, code, substance, reaction, severity) VALUES (19, 19, '300916003', 'Latex', 'Itching', 'Mild');
INSERT INTO AllergyIntolerances (id, patient_id, code, substance, reaction, severity) VALUES (20, 20, '416098002', 'Aspirin', 'Nausea', 'Moderate');
INSERT INTO AllergyIntolerances (id, patient_id, code, substance, reaction, severity) VALUES (21, 21, '91936005', 'Penicillin', 'Rash', 'Mild');
INSERT INTO AllergyIntolerances (id, patient_id, code, substance, reaction, severity) VALUES (22, 22, '91935009', 'Nuts', 'Anaphylaxis', 'Severe');
INSERT INTO AllergyIntolerances (id, patient_id, code, substance, reaction, severity) VALUES (23, 23, '213020009', 'Eggs', 'Hives', 'Moderate');
INSERT INTO AllergyIntolerances (id, patient_id, code, substance, reaction, severity) VALUES (24, 24, '300916003', 'Latex', 'Itching', 'Mild');
INSERT INTO AllergyIntolerances (id, patient_id, code, substance, reaction, severity) VALUES (25, 25, '416098002', 'Aspirin', 'Nausea', 'Moderate');

-- Insertar Medications (ejemplos SNOMED CT)
INSERT INTO Medications (id, patient_id, code, name, dosage, start_date, doctor_id) VALUES (1, 1, '387517004', 'Acetaminophen', '500mg', '2023-01-01', 1);
INSERT INTO Medications (id, patient_id, code, name, dosage, start_date, doctor_id) VALUES (2, 2, '387207008', 'Ibuprofen', '200mg', '2023-02-01', 2);
INSERT INTO Medications (id, patient_id, code, name, dosage, start_date, doctor_id) VALUES (3, 3, '387458008', 'Aspirin', '81mg', '2023-03-01', 3);
INSERT INTO Medications (id, patient_id, code, name, dosage, start_date, doctor_id) VALUES (4, 4, '372687004', 'Amoxicillin', '500mg', '2023-04-01', 4);
INSERT INTO Medications (id, patient_id, code, name, dosage, start_date, doctor_id) VALUES (5, 5, '372567009', 'Metformin', '1000mg', '2023-05-01', 5);
INSERT INTO Medications (id, patient_id, code, name, dosage, start_date, doctor_id) VALUES (6, 6, '387517004', 'Acetaminophen', '500mg', '2023-06-01', 1);
INSERT INTO Medications (id, patient_id, code, name, dosage, start_date, doctor_id) VALUES (7, 7, '387207008', 'Ibuprofen', '200mg', '2023-07-01', 2);
INSERT INTO Medications (id, patient_id, code, name, dosage, start_date, doctor_id) VALUES (8, 8, '387458008', 'Aspirin', '81mg', '2023-08-01', 3);
INSERT INTO Medications (id, patient_id, code, name, dosage, start_date, doctor_id) VALUES (9, 9, '372687004', 'Amoxicillin', '500mg', '2023-09-01', 4);
INSERT INTO Medications (id, patient_id, code, name, dosage, start_date, doctor_id) VALUES (10, 10, '372567009', 'Metformin', '1000mg', '2023-10-01', 5);
INSERT INTO Medications (id, patient_id, code, name, dosage, start_date, doctor_id) VALUES (11, 11, '387517004', 'Acetaminophen', '500mg', '2023-11-01', 1);
INSERT INTO Medications (id, patient_id, code, name, dosage, start_date, doctor_id) VALUES (12, 12, '387207008', 'Ibuprofen', '200mg', '2023-12-01', 2);
INSERT INTO Medications (id, patient_id, code, name, dosage, start_date, doctor_id) VALUES (13, 13, '387458008', 'Aspirin', '81mg', '2024-01-01', 3);
INSERT INTO Medications (id, patient_id, code, name, dosage, start_date, doctor_id) VALUES (14, 14, '372687004', 'Amoxicillin', '500mg', '2024-02-01', 4);
INSERT INTO Medications (id, patient_id, code, name, dosage, start_date, doctor_id) VALUES (15, 15, '372567009', 'Metformin', '1000mg', '2024-03-01', 5);
INSERT INTO Medications (id, patient_id, code, name, dosage, start_date, doctor_id) VALUES (16, 16, '387517004', 'Acetaminophen', '500mg', '2024-04-01', 1);
INSERT INTO Medications (id, patient_id, code, name, dosage, start_date, doctor_id) VALUES (17, 17, '387207008', 'Ibuprofen', '200mg', '2024-05-01', 2);
INSERT INTO Medications (id, patient_id, code, name, dosage, start_date, doctor_id) VALUES (18, 18, '387458008', 'Aspirin', '81mg', '2024-06-01', 3);
INSERT INTO Medications (id, patient_id, code, name, dosage, start_date, doctor_id) VALUES (19, 19, '372687004', 'Amoxicillin', '500mg', '2024-07-01', 4);
INSERT INTO Medications (id, patient_id, code, name, dosage, start_date, doctor_id) VALUES (20, 20, '372567009', 'Metformin', '1000mg', '2024-08-01', 5);
INSERT INTO Medications (id, patient_id, code, name, dosage, start_date, doctor_id) VALUES (21, 21, '387517004', 'Acetaminophen', '500mg', '2024-09-01', 1);
INSERT INTO Medications (id, patient_id, code, name, dosage, start_date, doctor_id) VALUES (22, 22, '387207008', 'Ibuprofen', '200mg', '2024-10-01', 2);
INSERT INTO Medications (id, patient_id, code, name, dosage, start_date, doctor_id) VALUES (23, 23, '387458008', 'Aspirin', '81mg', '2024-11-01', 3);
INSERT INTO Medications (id, patient_id, code, name, dosage, start_date, doctor_id) VALUES (24, 24, '372687004', 'Amoxicillin', '500mg', '2024-12-01', 4);
INSERT INTO Medications (id, patient_id, code, name, dosage, start_date, doctor_id) VALUES (25, 25, '372567009', 'Metformin', '1000mg', '2025-01-01', 5);

-- Insertar Coverages
INSERT INTO Coverages (id, patient_id, insurer, policy_number, start_date, end_date) VALUES (1, 1, 'Insurer A', 'POL001', '2023-01-01', '2024-12-31');
INSERT INTO Coverages (id, patient_id, insurer, policy_number, start_date, end_date) VALUES (2, 2, 'Insurer B', 'POL002', '2023-01-01', '2024-12-31');
INSERT INTO Coverages (id, patient_id, insurer, policy_number, start_date, end_date) VALUES (3, 3, 'Insurer C', 'POL003', '2023-01-01', '2024-12-31');
INSERT INTO Coverages (id, patient_id, insurer, policy_number, start_date, end_date) VALUES (4, 4, 'Insurer D', 'POL004', '2023-01-01', '2024-12-31');
INSERT INTO Coverages (id, patient_id, insurer, policy_number, start_date, end_date) VALUES (5, 5, 'Insurer E', 'POL005', '2023-01-01', '2024-12-31');
INSERT INTO Coverages (id, patient_id, insurer, policy_number, start_date, end_date) VALUES (6, 6, 'Insurer A', 'POL006', '2023-01-01', '2024-12-31');
INSERT INTO Coverages (id, patient_id, insurer, policy_number, start_date, end_date) VALUES (7, 7, 'Insurer B', 'POL007', '2023-01-01', '2024-12-31');
INSERT INTO Coverages (id, patient_id, insurer, policy_number, start_date, end_date) VALUES (8, 8, 'Insurer C', 'POL008', '2023-01-01', '2024-12-31');
INSERT INTO Coverages (id, patient_id, insurer, policy_number, start_date, end_date) VALUES (9, 9, 'Insurer D', 'POL009', '2023-01-01', '2024-12-31');
INSERT INTO Coverages (id, patient_id, insurer, policy_number, start_date, end_date) VALUES (10, 10, 'Insurer E', 'POL010', '2023-01-01', '2024-12-31');
INSERT INTO Coverages (id, patient_id, insurer, policy_number, start_date, end_date) VALUES (11, 11, 'Insurer A', 'POL011', '2023-01-01', '2024-12-31');
INSERT INTO Coverages (id, patient_id, insurer, policy_number, start_date, end_date) VALUES (12, 12, 'Insurer B', 'POL012', '2023-01-01', '2024-12-31');
INSERT INTO Coverages (id, patient_id, insurer, policy_number, start_date, end_date) VALUES (13, 13, 'Insurer C', 'POL013', '2023-01-01', '2024-12-31');
INSERT INTO Coverages (id, patient_id, insurer, policy_number, start_date, end_date) VALUES (14, 14, 'Insurer D', 'POL014', '2023-01-01', '2024-12-31');
INSERT INTO Coverages (id, patient_id, insurer, policy_number, start_date, end_date) VALUES (15, 15, 'Insurer E', 'POL015', '2023-01-01', '2024-12-31');
INSERT INTO Coverages (id, patient_id, insurer, policy_number, start_date, end_date) VALUES (16, 16, 'Insurer A', 'POL016', '2023-01-01', '2024-12-31');
INSERT INTO Coverages (id, patient_id, insurer, policy_number, start_date, end_date) VALUES (17, 17, 'Insurer B', 'POL017', '2023-01-01', '2024-12-31');
INSERT INTO Coverages (id, patient_id, insurer, policy_number, start_date, end_date) VALUES (18, 18, 'Insurer C', 'POL018', '2023-01-01', '2024-12-31');
INSERT INTO Coverages (id, patient_id, insurer, policy_number, start_date, end_date) VALUES (19, 19, 'Insurer D', 'POL019', '2023-01-01', '2024-12-31');
INSERT INTO Coverages (id, patient_id, insurer, policy_number, start_date, end_date) VALUES (20, 20, 'Insurer E', 'POL020', '2023-01-01', '2024-12-31');
INSERT INTO Coverages (id, patient_id, insurer, policy_number, start_date, end_date) VALUES (21, 21, 'Insurer A', 'POL021', '2023-01-01', '2024-12-31');
INSERT INTO Coverages (id, patient_id, insurer, policy_number, start_date, end_date) VALUES (22, 22, 'Insurer B', 'POL022', '2023-01-01', '2024-12-31');
INSERT INTO Coverages (id, patient_id, insurer, policy_number, start_date, end_date) VALUES (23, 23, 'Insurer C', 'POL023', '2023-01-01', '2024-12-31');
INSERT INTO Coverages (id, patient_id, insurer, policy_number, start_date, end_date) VALUES (24, 24, 'Insurer D', 'POL024', '2023-01-01', '2024-12-31');
INSERT INTO Coverages (id, patient_id, insurer, policy_number, start_date, end_date) VALUES (25, 25, 'Insurer E', 'POL025', '2023-01-01', '2024-12-31');