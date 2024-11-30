import re

from bridge.reply import Reply
from channel.chat_message import ChatMessage
import plugins.trpg.progress as pg
import plugins.trpg.model.user as user

input_test = (
    (".login admin", ".char use 橡皮", ".ra 智力"),
    (".ra 智力",),
    (".char gen",".char add xxx1")
)

msg=ChatMessage("")
msg.is_group=True
msg.actual_user_id="002"
msg.actual_user_nickname="橡皮"
reply=Reply()

user_id = None
if msg.is_group:
    user_id = msg.actual_user_id
else:
    user_id = msg.from_user_id
user_name = None
if msg.is_group:
    user_name = msg.actual_user_nickname
else:
    user_name = msg.from_user_nickname


def while_test():
    while True:
        context=input()
        if input == "exit":
            break
        context=pg.zh_to_eng(context)
        rd_regex = r'^\.r(\d)*d'
        ra_regex = r'^\.ra'
        char_regex = r'^\.char'
        login_regex = r'^\.login'
        register_regex = r'^\.register'
        if re.match(rd_regex, context):
            reply.content = pg.rd_process(user_name,user_id,context)
        if re.match(char_regex, context):
            reply.content = pg.char_process(user_name,user_id,context)
        if re.match(ra_regex, context):
            reply.content = pg.ra_process(user_name,user_id,context)
        if re.match(login_regex, context):
            reply.content = pg.login_process(user_name,user_id,context)
        if re.match(register_regex, context):
            reply.content = pg.register_process(user_name,user_id,context)
        print(reply.content)

while_test()



