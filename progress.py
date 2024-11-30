import re
from typing import Dict, List, Union

import plugins.trpg.tools.checkTree as cT
import plugins.trpg.tools.dice as dice
import plugins.trpg.tools.help as help
from channel.chat_message import ChatMessage
import plugins.trpg.model.character as character
import plugins.trpg.model.user as user
import plugins.trpg.tools.joking as joking

attributes_cache:Dict[int,character.Character]={}

def zh_to_eng(text):
    """
        将文本中的中文属性替换为英文缩写。

        Args:
            text: 需要替换的文本。

        Returns:
            替换后的文本。
        """

    pattern = r"力量|体质|体型|敏捷|外貌|智力|灵感|意志|教育|知识|幸运"
    replacements = {"力量": "STR", "体质": "CON", "体型": "SIZ",
                    "敏捷": "DEX", "外貌": "APP", "灵感": "INT", "智力": "INT",
                    "意志": "POW", "教育": "KNO", "知识": "KNO", "幸运": "LUC"}
    return re.sub(pattern, lambda m: replacements[m.group()], text)

def rd_process(context, msg):
    # step 1 pre analyse
    user_name = None
    if msg.is_group:
        user_name = msg.actual_user_nickname
    else:
        user_name = msg.from_user_nickname
    check_message=cT.check_rd(context)

    # step 2 process
    # step 2.1 error return
    if check_message.state==False:
        return "错误输入。 示例: .r[num]d[num][h|l]/.ra [STR|CON|SIZ|DEX|APP|INT|POW|KNO|LUC]"

    # step 2.2 generate
    dice_consequence1 = dice.generate_random_integers(check_message.parameters[0], check_message.parameters[1])
    dice_consequence2 = None
    if check_message.method == "h":
        dice_consequence2 = max(dice_consequence1)
    elif check_message.method == "l":
        dice_consequence2 = min(dice_consequence1)

    # step 2.3 reply
    miao_reply=""
    reply_str = f'执行{check_message.parameters[0]}d{check_message.parameters[1]}    '
    if check_message.method == "h":
        reply_str += f"惩罚骰:{str(dice_consequence2)}    "
        miao_reply="\n"+joking.return_joke(dice_consequence2,100)
    elif check_message.method == "l":
        reply_str += f"奖励骰:{str(dice_consequence2)}    "
        miao_reply = "\n" + joking.return_joke(dice_consequence2, 100)
    reply_str += f'{str(dice_consequence1)}'
    if check_message.parameters[0]==1:
        miao_reply = "\n" + joking.return_joke(dice_consequence2, 100)
    reply_str+=miao_reply
    return reply_str

def ra_process(context, msg):
    # step 1 pre analyse
    user_id = None
    if msg.is_group:
        user_id = msg.actual_user_id
    else:
        user_id = msg.from_user_id

    check_message=cT.check_ra(context)

    # step 2 process
    # step 2.1 error return
    if check_message.state==False:
        return "错误输入 示例: .ra [STR|CON|SIZ|DEX|APP|INT|POW|KNO|LUC|str]"
    # step 2.2 generate
    temp=dice.generate_random_integers(1,100)
    #step 2.2 reply
    miao_reply=""
    reply_str = f'执行ra {check_message.method}    '
    if check_message.method in character.Character.attribute_names:
        user_id = user.User.login_id(user_id)
        if user_id in attributes_cache and attributes_cache[user_id] is not None:
            temp=attributes_cache[user_id]
            reply_str+=f'{check_message.method} : {temp.get_attribute_value(check_message.method)}    '
            miao_reply="\n"+joking.return_joke(temp,temp.get_attribute_value(check_message.method))
        else:
            miao_reply = "\n" + joking.return_joke(temp, 100)
    reply_str += f'{temp}'
    reply_str+=miao_reply
    return reply_str

def char_process(context, msg:ChatMessage ):
    # step 1 pre analyse
    user_id=None
    if msg.is_group:
        user_id= msg.actual_user_id
    else:
        user_id= msg.from_user_id
    user_name = None
    if msg.is_group:
        user_name = msg.actual_user_nickname
    else:
        user_name = msg.from_user_nickname
    check_message=cT.check_char(context)

    # step 2 process
    # step 2.1 error return
    if check_message.state==False:
        return "错误输入 实例.char [add|use] [str]/.char edit [STR|CON|SIZ|DEX|APP|INT|POW|KNO|LUC] [num]/.char gen/.char show"
    if not user.User.is_logined(user_id):
        return "请先登录或注册 实例: .login [str]/.register"
    user_id = user.User.login_id(user_id)
    #step 2.2 reply
    if check_message.method == "add":
        if user_id in attributes_cache and attributes_cache[user_id] is not None:
            attributes_cache[user_id].name=check_message.parameters[0]
            temp=attributes_cache[user_id].save_to_db()
            if temp is not None:
                return temp
            else:
                return "角色已加入"
        else:
            return "没有已生成数据"
    elif check_message.method == "use":
        temp=character.Character.load_from_db(check_message.parameters[0],user_id)
        if temp is not None:
            attributes_cache[user_id]=temp
            return attributes_cache[user_id].print_character_info()
        else:
            return "不存在指定角色"
    elif check_message.method == "edit":
        if user_id in attributes_cache and attributes_cache[user_id] is not None:
            temp=attributes_cache[user_id].update_attribute(check_message.parameters[0],check_message.parameters[1])
            if temp is not None:
                return temp
            else:
                return attributes_cache[user_id].print_character_info()
        return
    elif check_message.method == "gen":
        attributes_cache[user_id] = character.Character.generate_random_character("temp_"+user_name,user_id)
        return attributes_cache[user_id].print_character_info()
    elif check_message.method == "show":
        temp=character.Character.query_by_owner(user_id)
        if temp is not  None:
            reply_str=f"\n{'_'*13}\n"
            for i in temp:
                reply_str+=f'{i:^13}\n'
            reply_str += f"{'_' * 13}\n"
            return reply_str
        return "未创建角色"

def login_process(context, msg):
    user_id = None
    if msg.is_group:
        user_id = msg.actual_user_id
    else:
        user_id = msg.from_user_id

    method=cT.check_login(context)
    if method.state==False:
        return "密码错误"
    else:
        return user.User.login(method.method,user_id)


def register_process(context, msg):
    user_id = None
    if msg.is_group:
        user_id = msg.actual_user_id
    else:
        user_id = msg.from_user_id

    return user.User.register(user_id)

def help_process(context, msg):
    return help.help_info()
