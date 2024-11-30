# encoding:utf-8
import re

import plugins
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from plugins import *
import plugins.trpg.progress as pg


@plugins.register(
    name="Trpg",
    desire_priority=100,
    desc="Being locked in a black room",
    version="0.1",
    author="augustus0508",
)
class Trpg(Plugin):
    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        logger.info("[Finish] inited")

    def on_handle_context(self, e_context: EventContext):
        if e_context['context'].type != ContextType.TEXT:
            return
        # todo 拿到context
        # rd_regex = r'^\.r\d*d\d*( )*((-)( )*(h|l))?$'
        context = e_context["context"].content
        context = pg.zh_to_eng(context)
        # todo 编辑返回值
        msg= e_context['context']['msg']
        reply = Reply()
        reply.type = ReplyType.TEXT

        # todo process
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

        rd_regex = r'^\.r(\d)*d'
        ra_regex = r'^\.ra'
        char_regex = r'^\.char'
        login_regex = r'^\.login'
        register_regex = r'^\.register'
        help_regex = r'^\.help'
        if re.match(rd_regex, context):
            reply.content = pg.rd_process(user_name,user_id,context)
        elif re.match(char_regex, context):
            reply.content = pg.char_process(user_name,user_id,context)
        elif re.match(ra_regex, context):
            reply.content = pg.ra_process(user_name,user_id,context)
        elif re.match(login_regex, context):
            reply.content = pg.login_process(user_name,user_id,context)
        elif re.match(register_regex, context):
            reply.content = pg.register_process(user_name,user_id,context)
        elif re.match(help_regex, context):
            reply.content = pg.help_process()
        else:
            e_context['reply'] = reply
            e_context.action = EventAction.CONTINUE
            return
        e_context['reply'] = reply
        e_context.action = EventAction.BREAK_PASS
        return