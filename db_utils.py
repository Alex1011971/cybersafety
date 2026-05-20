import os
import sqlite3

DB_PATH = 'cyber_security.db'
DOCS_DIR = 'instructions'

def init_db():
    """Создает БД и загружает в нее данные из текстовых файлов"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS instructions 
                      (id INTEGER PRIMARY KEY, title TEXT, content TEXT, keywords TEXT)''')
    
    cursor.execute("SELECT COUNT(*) FROM instructions")
    if cursor.fetchone()[0] == 0:
        if os.path.exists(DOCS_DIR):
            for filename in os.listdir(DOCS_DIR):
                if filename.endswith('.txt'):
                    title = filename.replace('.txt', '')
                    with open(os.path.join(DOCS_DIR, filename), 'r', encoding='utf-8') as f:
                        content = f.read()
                    keywords = title.lower() 
                    cursor.execute("INSERT INTO instructions (title, content, keywords) VALUES (?, ?, ?)",
                                   (title, content, keywords))
            conn.commit()
    conn.close()

def get_all_instructions():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM instructions")
    results = cursor.fetchall()
    conn.close()
    return results

def get_instruction_by_id(instr_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT title, content FROM instructions WHERE id=?", (instr_id,))
    result = cursor.fetchone()
    conn.close()
    return result

def search_instructions(query):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM instructions WHERE title LIKE ? OR keywords LIKE ?", 
                   (f'%{query}%', f'%{query}%'))
    results = cursor.fetchall()
    conn.close()
    return results