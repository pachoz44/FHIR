import sqlite3

# Conectar a la base de datos (se crea si no existe)
conn = sqlite3.connect('hospital_A.db')
cursor = conn.cursor()

# Leer el contenido del archivo SQL
with open('sql_script.sql', 'r', encoding='utf-8') as f:
    sql_script = f.read()

# Ejecutar el script
cursor.executescript(sql_script)

# Confirmar cambios y cerrar
conn.commit()
conn.close()

print("Base de datos creada exitosamente.")