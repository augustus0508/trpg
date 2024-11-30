import sqlite3

from plugins.trpg.database import sql_url


def insert_into_usertochar(name, owner, str, con, siz, dex, app, int, pow, kon, luc):
    """
    将数据插入到 userTochar 表中。

    Args:
        name: 用户名
        owner: 所有者
        str: STR 属性
        con: CON 属性
        siz: SIZ 属性
        dex: DEX 属性
        app: APP 属性
        int: INT 属性
        pow: POW 属性
        kon: KNO 属性
        luc: LUC 属性
    """
    conn = sqlite3.connect(sql_url)
    cursor = conn.cursor()
    sql = "SELECT name FROM userChar WHERE owner = ?"
    results = cursor.execute(sql, (owner,)).fetchall()
    results = [i[0] for i in results]
    if name not in results:
        sql = """
            INSERT INTO userChar (
                name, owner, STR, CON, SIZ, DEX, APP, INT, POW, KNO, LUC
            ) VALUES (
                ?,?,?,?,?,?,?,?,?,?,?
            )
        """
        cursor.execute(sql, (name, owner, str, con, siz, dex, app, int, pow, kon, luc))
        conn.commit()
        conn.close()
    else:
        conn.close()
        raise Exception("重复名称")


def update_user_attribute(name, owner, attribute, new_value):
    """
    更新指定用户的属性值。

    Args:
        name: 用户名
        owner: 所有者
        attribute: 要修改的属性名 (str)
        new_value: 新的属性值

    Raises:
        ValueError: 如果属性名无效或数据类型不匹配
    """
    conn = sqlite3.connect(sql_url)
    # 校验属性名
    valid_attributes = ('STR', 'CON', 'SIZ', 'DEX', 'APP', 'INT', 'POW', 'KNO', 'LUC')
    if attribute not in valid_attributes:
        raise ValueError(f"Invalid attribute: {attribute}")

    # 执行更新操作
    cursor = conn.cursor()
    sql = f"UPDATE userChar SET {attribute} = ? WHERE name = ? AND owner = ?"
    cursor.execute(sql, (new_value, name, owner))
    conn.commit()
    conn.close()

def query_by_owner(owner):
    """
    根据owner查拥有角色

    """
    conn = sqlite3.connect(sql_url)
    cursor = conn.cursor()
    sql = "SELECT name FROM userChar WHERE owner = ?"
    results = cursor.execute(sql, (owner,)).fetchall()
    conn.close()
    return [i[0] for i in results]

def query_by_owner_and_user(name ,owner):
    """
    根据owner和user查询数据。

    Args:
        conn: 数据库连接对象
        owner: 所有者
        name: 用户名

    Returns:
        查询结果列表，每个元素是一个元组，表示一条记录。
    """
    conn = sqlite3.connect(sql_url)
    cursor = conn.cursor()
    sql = "SELECT name,owner,STR,CON,SIZ,DEX,APP,INT,POW,KNO,LUC FROM userChar WHERE owner = ? AND name = ?"
    results = cursor.execute(sql, (owner, name)).fetchall()
    conn.close()
    return results


