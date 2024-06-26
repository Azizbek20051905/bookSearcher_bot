from typing import Any
from aiogram.filters import Filter
from aiogram.types import Message
from core.db_api.DB import get_chennel_api
from aiogram import Bot
from core.settings import settings

class CheckSubChannel(Filter):
    async def __call__(self, message: Message, bot: Bot):
        channel_list = []
        channels = get_chennel_api()
        
        for channel in channels:
            links = str(channel['link']).replace('https://t.me/', '@')

            user_status = await bot.get_chat_member(str(links), message.from_user.id)
            
            if user_status.status in ['member', 'administrator', "creator"]:
                channel_list.append(False)
            else:
                channel_list.append(True)
        
        if True not in channel_list:
            return False
        else:
            return True