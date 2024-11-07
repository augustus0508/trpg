import plugins.trpg.tool.checkTree as cT
import plugins.trpg.tool.dice as dice
from lib.itchat.storage.messagequeue import logger


def rd_process(context, msg):
    # pre analyse
    method=cT.check_rd(context)
    if method.state==False:
        return "错误输入。 实例： .r[num]d[num][h|l]"
    # generate
    dice_consequence1 = dice.generate_random_integers(method.parameters[0], method.parameters[1])
    dice_consequence2 = None
    if method.method == "h":
        dice_consequence2 = max(dice_consequence1)
    elif method.method == "l":
        dice_consequence2 = min(dice_consequence1)

    # reply

    reply_str = f'执行{method.parameters[0]}d{method.parameters[1]}\n'
    if method.method == "h":
        reply_str += f"奖励骰:{str(dice_consequence2)}\n"
    elif method.method == "l":
        reply_str += f"惩罚骰:{str(dice_consequence2)}\n"
    if msg.is_group:
        reply_str += f'用户{msg.actual_user_nickname}'
    else:
        reply_str += f'用户{msg.from_user_nickname}'
    reply_str += f'{str(dice_consequence1)}'
    return reply_str


def char_process(context, msg, ):
    reply_str = ""
    return reply_str
