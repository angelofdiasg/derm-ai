import sqlite3
from datetime import date

def salvar_consulta(patient_id, transcricao, analise):

    conn = sqlite3.connect("derm_ai.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO consultas (patient_id, data_consulta, transcricao, analise)
    VALUES (?, ?, ?, ?)
    """, (
        patient_id,
        date.today().strftime("%Y-%m-%d"),
        transcricao,
        analise
    ))

    conn.commit()
    conn.close()