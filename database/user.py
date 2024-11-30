import sqlite3
from plugins.trpg.database import sql_url


def load_user(password):
    # 连接数据库
    conn = sqlite3.connect(sql_url)
    cursor = conn.cursor()
    # 执行查询
    cursor.execute('SELECT * FROM passwordid WHERE password = ?', (password,))
    result = cursor.fetchone()
    conn.close()

    return result

def add_user(password,id):
    conn = sqlite3.connect(sql_url)
    cursor = conn.cursor()
    # 执行查询
    try:
        cursor.execute("INSERT INTO passwordid (password,id) VALUES (?, ?)", (password,id))
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError as e:
        conn.close()
        return e
    return

def update_user(password,id):
    conn = sqlite3.connect(sql_url)
    cursor = conn.cursor()
    # 执行查询
    cursor.execute("UPDATE passwordid SET id = ? WHERE password = ?", (password, id))
    conn.commit()
    conn.close()
    return