import re

from bridge.reply import Reply
from channel.chat_message import ChatMessage
import plugins.trpg.progress as pg

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
while True:
    context=input()
    context=pg.zh_to_eng(context)
    rd_regex = r'^\.r(\d)*d'
    ra_regex = r'^\.ra'
    char_regex = r'^\.char'
    login_regex = r'^\.login'
    register_regex = r'^\.register'
    if re.match(rd_regex, context):
        reply.content = pg.rd_process(context, msg)
    if re.match(char_regex, context):
        reply.content = pg.char_process(context, msg)
    if re.match(ra_regex, context):
        reply.content = pg.ra_process(context, msg)
    if re.match(login_regex, context):
        reply.content = pg.login_process(context, msg)
    if re.match(register_regex, context):
        reply.content = pg.register_process(context, msg)
    print(reply.content)




