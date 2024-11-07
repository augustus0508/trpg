# encoding:utf-8
import re

import plugins
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from common.log import logger
from config import conf
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
        # todo 规定正则
        # rd_regex = r'^\.r\d*d\d*( )*((-)( )*(h|l))?$'
        rd_regex = r'^\.r'
        char_regex = r'^\.char'
        context = e_context["context"].content
        # todo 编辑返回值
        msg= e_context['context']['msg']
        reply = Reply()
        reply.type = ReplyType.TEXT
        if re.match(rd_regex, context):
            reply.content=pg.rd_process(context,msg)
        e_context['reply'] = reply
        e_context.action = EventAction.BREAK_PASS
        return