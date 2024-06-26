import json
from aiogram import Bot, types
from aiogram.types import Message, FSInputFile, InputMediaVideo, InputMediaPhoto
# from aiogram.utils.chat_action import ChatActionSender
from core.db_api.DB import get_book_search, get_top_books_api, get_mylikes_api, post_books_api
from core.keyboards.inline import  get_channel_keyboard, admin_btn, get_inline_keyboard, top_inline_keyboard, like_inline_keyboard
# from core.keyboards.reply import button
# from core.states.states import GetId

from core.utils.callbackdata import NextLine
from core.settings import settings

async def post_books(message: Message, bot: Bot):
    name=message.document.file_name
    file_id=message.document.file_id
    file_type="document"

    text = f"""Kitob qo'shildi: {name}"""

    await bot.send_message(chat_id=settings.bots.admin_id, text=text)
    post_books_api(name=name, file_id=file_id, file_type=file_type)

async def post_books_audio(message: Message, bot: Bot):
    name=message.audio.file_name
    file_id=message.audio.file_id
    file_type="audio"

    text = f"""Audio Kitob qo'shildi: {name}"""

    await bot.send_message(chat_id=settings.bots.admin_id, text=text)
    post_books_api(name=name, file_id=file_id, file_type=file_type)


async def sub_channel_answer(message: Message):
    await message.answer(f"Iltimos, kanalga obuna bo'ling va qayta urinib ko'ring.", parse_mode="HTML", reply_markup=get_channel_keyboard())

async def get_search(message: types.Message, bot: Bot):
    books = get_book_search(message.text)
    if books:
        names = get_inline_keyboard(books=books, user_id=message.chat.id, searches=message.text)
        await message.reply(text=f"⬇️ Qidiruv natijalari:", reply_markup=names)
    else:
        await message.reply(text="🙁Afsuski natija topilmadi.")

async def top_books(message: types.Message, bot: Bot):
    inline=top_inline_keyboard(get_top_books_api())
    await message.reply(text="🔝Top 10 mashhur kitoblar: ", reply_markup=inline)

async def get_my_likes(message: types.Message, bot: Bot):
    user_id = message.chat.id

    like_books = get_mylikes_api(user_id)

    if like_books['status'] == 'success':
        inline = like_inline_keyboard(user_id=user_id, books=like_books['like_book'])
        await message.reply(text="❤️Siz yoqtirgan kitoblar: ", reply_markup=inline)
    else:
        await message.reply(text="Sizning yoqtirgan kitoblaringiz mavjud emas❗")

async def AdminPanel(message: types.Message, bot: Bot):
    user_id = message.from_user.id

    if int(settings.bots.admin_id) == int(user_id):
        btn_admin = admin_btn()
        await message.reply(text="Xush kelibsiz bratim ", reply_markup=btn_admin)

