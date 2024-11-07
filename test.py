import re

from channel.chat_message import ChatMessage
import plugins.trpg.progress as pg

msg=ChatMessage("")
msg.is_group=True
context=input()
content=""
rd_regex = r'^\.r'
char_regex = r'^\.char'

if re.match(rd_regex, context):
    content = pg.rd_process(context, msg)

print(content)
