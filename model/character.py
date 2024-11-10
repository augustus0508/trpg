import random

from web import database

import plugins.trpg.database.player as player

class Character:
    attribute_names = ["STR", "CON", "SIZ", "DEX", "APP", "INT", "POW", "KNO", "LUC"]
    def __init__(self, name, owner, STR, CON, SIZ, DEX, APP, INT, POW, KNO, LUC):
        self.name = name
        self.owner = owner
        self.STR = STR
        self.CON = CON
        self.SIZ = SIZ
        self.DEX = DEX
        self.APP = APP
        self.INT = INT
        self.POW = POW
        self.KNO = KNO
        self.LUC = LUC

    def save_to_db(self):
        """将角色数据插入到数据库中"""
        try:
            player.insert_into_usertochar(self.name, self.owner, self.STR, self.CON,
                                          self.SIZ, self.DEX, self.APP, self.INT,
                                          self.POW, self.KNO, self.LUC)
        except Exception as e:
            return str(e)

    def update_attribute(self, attribute, new_value):
        """更新角色的属性"""
        try:
            player.update_user_attribute(self.name, self.owner, attribute, new_value)
            setattr(self, attribute, new_value)
        except Exception as e:
            return str(e)

    def get_attribute_value(self, attribute_name):
        """
        根据属性字符串返回对应属性值。

        Args:
          character: Character对象。
          attribute_name: 要获取属性的名称。

        Returns:
          属性值，如果属性不存在则返回None。
        """

        # 检查属性名称是否有效
        if attribute_name not in Character.attribute_names:
            return None

        # 使用getattr获取属性值
        return getattr(self, attribute_name)

    def print_character_info(self):
        """
        打印角色信息，以表格形式展示。

        Args:
            self: Character对象本身。
        """

        reply_str=""
        # 打印顶部框
        reply_str+=f'\n{"-" * 27}\n'
        reply_str+=f" {self.name: ^22}  \n"
        reply_str+=f'{"-" * 27}\n'

        # 打印属性表格
        for i in range(0, len(Character.attribute_names), 2):
            attr1 = Character.attribute_names[i]
            attr2 = Character.attribute_names[i + 1] if i + 1 < len(Character.attribute_names) else ""
            reply_str+=f"| {attr1:<10} | {getattr(self, attr1):>10} |\n"
            if attr2 != "":
                reply_str+=f"| {attr2:<10} | {getattr(self, attr2):>10} |\n"

        # 打印底部框
        reply_str+=f'{"-" * 27}\n'
        return reply_str

    @classmethod
    def load_from_db(cls, name ,owner):
        """从数据库中加载角色数据"""
        data = player.query_by_owner_and_user(name, owner)
        if data:
            return cls(*data[0])
        return None

    @classmethod
    def query_by_owner(cls, owner):
        data=player.query_by_owner(owner)
        if data:
            return data
        return None

    @classmethod
    def generate_random_character(cls,name,owner):
        """
        随机生成一个Character对象。

        Args:
            owner: 角色的所有者。

        Returns:
            Character: 生成的角色对象。
        """


        # 随机生成属性值（0-100，步长为5）
        attributes = [random.choice(range(10, 101, 5)) for _ in range(9)]

        # 创建Character对象
        character = cls(
            name=name,
            owner=owner,
            STR=attributes[0],
            CON=attributes[1],
            SIZ=attributes[2],
            DEX=attributes[3],
            APP=attributes[4],
            INT=attributes[5],
            POW=attributes[6],
            KNO=attributes[7],
            LUC=attributes[8]
        )
        return character