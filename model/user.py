from typing import Dict, List, Union
import random
import string
import plugins.trpg.database.user as pw
from plugins.trpg.database.user import update_user


def generate_random_string(length):
    """生成指定长度的随机字符串，包含数字、大小写字母和符号。

    Args:
        length: 字符串长度。

    Returns:
        生成的随机字符串。
    """

    characters = string.digits + string.ascii_letters + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

class User:
    idPassword: Dict[str,str]={}#表示微信id到login_id的变化
    def __init__(self):
        return
    @classmethod
    def login(cls,password,id):
        temp=pw.load_user(password)
        if temp:
            update_user(password,id)
            cls.idPassword[id]=password
            return f"成功登录:{password}"
        else:
            return "密码错误"

    @classmethod
    def register(cls,id):
        if id in cls.idPassword:
            return "请勿重复注册"
        else:
            while True:
                password=generate_random_string(6)
                e=pw.add_user(password,id)
                if e is not None:
                    continue
                else:
                    cls.idPassword[id] = password
                    return f"注册成功,请记住登录口令： \"{password}\""

    @classmethod
    def is_logined(cls,id):
        return id in cls.idPassword

    @classmethod
    def login_id(cls,id):
        if cls.is_logined(id):
            return cls.idPassword[id]
        else:
            return "admin"


