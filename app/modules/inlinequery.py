#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from uuid import uuid4
from telegram import InlineQueryResultArticle, InputTextMessageContent, ParseMode
from ..utils.logging import logger
from ..sources import wf as wf


def warframe_inline_query(update, context):
    inline_query = update.inline_query
    from_user = inline_query.from_user
    query = inline_query.query
    logger.info(f"@@@@ inline_query from user [{from_user.username} ({from_user.id})] msg: {query}")
    input_message_content = InputTextMessageContent(wf.get_invasions(from_user.id), parse_mode=ParseMode.MARKDOWN)
    results = [
        InlineQueryResultArticle(id=uuid4(),
                                 title='All Active Invasions',
                                 thumb_url='https://imgur.com/qO0rcCI.png',
                                 description='List of all Warframe invasions',
                                 input_message_content=input_message_content
                                 )
        ]
    update.inline_query.answer(results)
