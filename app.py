from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.enums import ParseMode

from core.handlers.basic import sub_channel_answer, AdminPanel, get_search, top_books, get_my_likes, post_books, post_books_audio
from core.handlers.callback import (select_books, select_audio, posted_channel, delete_answer, like_answer, 
                                    dislike_answer, next_book, next_booklikes, update_message, update_title, channel_name, channel_link, channel_delete, channel_edit)
from core.filters.filter import CheckSubChannel
from core.utils.commands import set_commands, set_commands_admin
from core.settings import settings
from core.utils.callbackdata import DeleteMessage, BookInfo, LikeMessage, NextLine, PreviousLine, DeleteChannel

from aiogram.fsm.storage.memory import MemoryStorage
from core.states.states import UpdateMessage, ChannelsLink


import asyncio
import logging


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, text="Bot ishga tushdi!")
        

async def get_start(message: types.Message, bot: Bot):
    text = f"🖐<b>Assalomu Alaykum,</b> <a href='tg://user?id={message.from_user.id}'>{message.from_user.full_name}</a>\n\n"\
            f"<blockquote>📖 Sizga istalgan turdagi kitoblarni izlashda yordam beraman.\n"\
            "/start - ♻️Botni Yangilash."\
            "\n/help - 🎛Barcha buyruqlar."\
            "\n/top - 📚Ko'p yuklab olingan kitoblar."\
            "\n/my_like - ❤️Sevimli kitoblar.</blockquote>"\
            "\n🔎 Kerakli kitob nomini yozib yuboring:"\
    
    await message.answer(text=text)

async def get_help(message: types.Message, bot: Bot):
    text = f"🖐<b>Assalomu Alaykum,</b> <a href='tg://user?id={message.from_user.id}'>{message.from_user.full_name}</a>\n\n"\
            f"""<blockquote>🆘Buyruqlar Ro'yhati\n
/start - ♻️Botni Yangilash.\n/help - 🎛Barcha buyruqlar.\n/top - 📚Ko'p yuklab olingan kitoblar.\n/my_like - ❤️Sevimli kitoblar.</blockquote>\n\n🔎 Kerakli kitob nomini yozib yuboring:"""
    
    await message.answer(text=text)

async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text="Bot to'xtadi!")


async def start():
    logging.basicConfig(filename="./warning_bot/warning.log",
                        filemode='a',
                        format="asctime == %(asctime)s |||------------|||\n levelname == [%(levelname)s] |||-----------|||\n name == %(name)s |||------------|||\n msecs - %(msecs)d -------\n "
                            "Filename and funcName == (%(filename)s).(%(funcName)s)\n lineno == (%(lineno)d)\n message == %(message)s",
                        datefmt='%D:%H:%M:%S',
                        level=logging.WARNING,
                            )
    bot = Bot(token=settings.bots.bot_token, parse_mode="HTML")

    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    dp.startup.register(start_bot)

    dp.channel_post.register(post_books, F.document)
    dp.channel_post.register(post_books_audio, F.audio)
    # dp.callback_query.register(prev_book, NextLine.filter(F.model == 'prev'))
    dp.callback_query.register(update_message, PreviousLine.filter(F.model == 'messages'))
    dp.callback_query.register(posted_channel, PreviousLine.filter(F.model == 'add_channel'))
    dp.callback_query.register(channel_delete, PreviousLine.filter(F.model == 'delete_channel'))
    dp.callback_query.register(channel_edit, DeleteChannel.filter(F.model == 'delete_channel_entry'))
    dp.callback_query.register(next_book, NextLine.filter(F.model == 'next'))
    dp.callback_query.register(next_booklikes, NextLine.filter(F.model == 'next_like'))
    dp.callback_query.register(select_books, BookInfo.filter(F.file_type == 'document'))
    dp.callback_query.register(select_audio, BookInfo.filter(F.file_type == 'audio'))
    dp.callback_query.register(like_answer, LikeMessage.filter(F.model == 'like'))
    dp.callback_query.register(dislike_answer, LikeMessage.filter(F.model == 'dislike'))
    dp.callback_query.register(delete_answer, DeleteMessage.filter(F.model == 'delete'))
    dp.message.register(sub_channel_answer, CheckSubChannel())
    dp.message.register(update_title, UpdateMessage.title)
    dp.message.register(channel_name, ChannelsLink.name)
    dp.message.register(channel_link, ChannelsLink.link)
    dp.message.register(get_start, Command(commands='start'))
    dp.message.register(get_help, Command(commands='help'))
    dp.message.register(top_books, Command(commands='top'))
    dp.message.register(get_my_likes, Command(commands='my_like'))
    dp.message.register(AdminPanel, Command(commands='admin_panel'))
    dp.message.register(get_search, F.text)
    
    dp.shutdown.register(stop_bot)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(start())