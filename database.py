import sqlite3

def conectar():
    return sqlite3.connect("derm_ai.db")

def criar_tabelas():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        email TEXT,
        senha TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        nome TEXT,
        sexo TEXT,
        data_nascimento TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS consultas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        data_consulta TEXT,
        transcricao TEXT,
        analise TEXT
    )
    """)

    conn.commit()
    conn.close()