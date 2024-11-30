import re
from typing import Dict, List, Union

import plugins.trpg.tools.checkTree as cT
import plugins.trpg.tools.dice as dice
import plugins.trpg.tools.help as help
import plugins.trpg.model.character as character
import plugins.trpg.model.user as user
import plugins.trpg.tools.joking as joking

attributes_cache:Dict[str,character.Character]={} #id2char,正在使用的角色

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

def rd_process(user_name,user_id,context):
    # step 1 pre analyse
    check_message=cT.check_rd(context)

    # step 2 process
    # step 2.1 error return
    if check_message.state==False:
        return "Error: 示例: .r[num]d[num][h|l]/.ra [STR|CON|SIZ|DEX|APP|INT|POW|KNO|LUC]"

    # step 2.2 generate
    dice_consequence1 = dice.generate_random_integers(check_message.parameters[0], check_message.parameters[1])
    dice_consequence2 = None
    if check_message.method == "h":
        dice_consequence2 = [max(dice_consequence1),]
    elif check_message.method == "l":
        dice_consequence2 = [min(dice_consequence1),]

    # step 2.3 reply
    reply_str = f'执行{check_message.parameters[0]}d{check_message.parameters[1]}    '
    miao_reply=""

    if check_message.method == "h":
        reply_str += f"惩罚骰:{str(dice_consequence2)}    "
        miao_reply="\n"+joking.return_joke(dice_consequence2,check_message.parameters[1])
    elif check_message.method == "l":
        reply_str += f"奖励骰:{str(dice_consequence2)}    "
        miao_reply = "\n" + joking.return_joke(dice_consequence2, check_message.parameters[1])
    elif check_message.parameters[0]==1:
        miao_reply = "\n" + joking.return_joke(dice_consequence1, check_message.parameters[1])

    reply_str += f'{dice_consequence1}'
    reply_str+=miao_reply

    return reply_str

def ra_process(user_name,user_id,context):
    # step 1 pre analyse
    check_message=cT.check_ra(context)

    # step 2 process
    # step 2.1 error return
    if check_message.state==False:
        return "Error: 示例: .ra [STR|CON|SIZ|DEX|APP|INT|POW|KNO|LUC|str]"
    # step 2.2 generate
    temp_dice=dice.generate_random_integers(1,100)

    #step 2.2 reply
    reply_str = f'执行ra {check_message.method}    '
    miao_reply=""

    if check_message.method in character.Character.attribute_names:
        user_id = user.User.login_id(user_id)#默认取到admin
        if user_id in attributes_cache and attributes_cache[user_id] is not None:
            temp_char=attributes_cache[user_id]
            reply_str+=f'{check_message.method} : {temp_char.get_attribute_value(check_message.method)}    '
            miao_reply="\n"+joking.return_joke(temp_dice,temp_char.get_attribute_value(check_message.method))
        else:
            miao_reply = "\n" + joking.return_joke(temp_dice, 100)
    else:
        miao_reply = "\n" + joking.return_joke(temp_dice, 100)

    reply_str += f'{temp_dice}'
    reply_str+=miao_reply

    return reply_str

def char_process(user_name, user_id, context):
    # step 1 pre analyse
    check_message=cT.check_char(context)

    # step 2 process
    # step 2.1 error return
    if check_message.state==False:
        return "Error: 示例.char [add|use] [str]/.char edit [STR|CON|SIZ|DEX|APP|INT|POW|KNO|LUC] [num]/.char gen/.char show"
    if not user.User.is_logined(user_id):
        return "Error: 请先登录或注册 实例: .login [str]/.register"

    # step 2.2 replace user_id to login_user_id
    login_user_id = user.User.login_id(user_id)

    # step 2.3 reply
    if check_message.method == "add":
        if login_user_id in attributes_cache and attributes_cache[login_user_id] is not None:
            attributes_cache[login_user_id].name=check_message.parameters[0]
            err=attributes_cache[login_user_id].save_to_db()
            if err is not None:
                return err
            return "角色已加入"
        else:
            return "Error: 没有已生成数据"
    elif check_message.method == "use":
        err,data=character.Character.load_from_db(check_message.parameters[0], login_user_id)
        if err is not None:
            return err

        if data is not None:
            attributes_cache[login_user_id]=err
            return attributes_cache[login_user_id].print_character_info()
        else:
            return "Error: 不存在指定角色"
    elif check_message.method == "edit":
        if login_user_id in attributes_cache and attributes_cache[login_user_id] is not None:
            err=attributes_cache[login_user_id].update_attribute(check_message.parameters[0], check_message.parameters[1])
            if err is not None:
                return err
            return attributes_cache[login_user_id].print_character_info()
    elif check_message.method == "gen":
        attributes_cache[login_user_id] = character.Character.generate_random_character("temp_" + user_name, login_user_id)
        return attributes_cache[login_user_id].print_character_info()
    elif check_message.method == "show":
        err,data=character.Character.query_by_owner(login_user_id)
        if err is not None:
            return err

        if data is not  None:
            reply_str=f"\n{'_'*13}\n"
            for i in data:
                reply_str+=f'{i:^13}\n'
            reply_str += f"{'_' * 13}\n"
            return reply_str
        return "Error: 未创建角色"

def login_process(user_name,user_id,context):
    method=cT.check_login(context)
    if method.state==False:
        return "Error: 密码错误"
    else:
        return user.User.login(method.method,user_id)


def register_process(user_name,user_id,context):
    return user.User.register(user_id)

def help_process():
    return help.help_info()
