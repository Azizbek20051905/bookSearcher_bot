from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from core.utils.callbackdata import BookInfo, DeleteMessage, LikeMessage, DeleteChannel
from core.db_api.DB import (get_book_details_api, put_book_details_api, put_message_api, 
                            get_message_api, post_mylikes_api, get_mylikes_api, delete_mylikes_api, 
                            get_book_search, post_chennel_api, get_chennel_api, delete_channel_api)
from core.keyboards.inline import likes, next_button, next_like_button, stop_channel, get_channel_button
from core.states.states import UpdateMessage, ChannelsLink

from core.utils.callbackdata import NextLine


# book selection
async def select_books(call: CallbackQuery, bot: Bot, callback_data: BookInfo):
    id = callback_data.file_id
    books = get_book_details_api(pk=id)["book"]
    message = get_message_api()[0]['text']
    user_id = call.message.chat.id
    print(message)
    
    await call.message.reply_document(document=books['file_id'], caption=f"<blockquote>📚Name: {books['name']}</blockquote>\n\n<b>{message}</b>", reply_markup=likes(tg_id=user_id, book_id=id))

async def select_audio(call: CallbackQuery, bot: Bot, callback_data: BookInfo):
    id = callback_data.file_id
    books = get_book_details_api(pk=id)["book"]
    message = get_message_api()[0]['text']
    user_id = call.message.chat.id
    
    await call.message.reply_audio(audio=books['file_id'], caption=f"<blockquote>📚Name: {books['name']}</blockquote>\n\n<b>{message}</b>", reply_markup=likes(tg_id=user_id, book_id=id))


async def delete_answer(call: CallbackQuery, bot: Bot, callback_data: DeleteMessage):
    await bot.delete_message(chat_id = call.message.chat.id, message_id=call.message.message_id)

async def like_answer(call: CallbackQuery, bot: Bot, callback_data: LikeMessage):
    user_id = callback_data.telegram_id
    book_id = callback_data.books
    model = callback_data.model

    messages = get_mylikes_api(user_id=user_id)
    status = messages['status']
    print()
    print(messages)
    print()

    if status == 'success':
        for message in messages['like_book']:
            if int(message['books']) == book_id:
                resault = False
                break
            else:
                resault = True
        
        if resault:
            natija = post_mylikes_api(user_id=user_id, book_id=book_id)
            add_like = put_book_details_api(pk=book_id, number=1)
            await bot.answer_callback_query(call.id, text='❤️Kitob yoqtirilganlar ro\'yxatiga qo\'shildi', show_alert=False)

        await bot.answer_callback_query(call.id, text='❤️Kitob yoqtirilganlar ro\'yxatiga qo\'shildi', show_alert=False)
    else:
        resault = post_mylikes_api(user_id=user_id, book_id=book_id)
        add_like = put_book_details_api(pk=book_id, number=1)
        await bot.answer_callback_query(call.id, text='❤️Kitob yoqtirilganlar ro\'yxatiga qo\'shildi', show_alert=False)

    # await call.message.answer(text='❤️Kitob yoqtirilganlar ro\'yxatiga qo\'shildi', show_alert=True)

async def dislike_answer(call: CallbackQuery, bot: Bot, callback_data: LikeMessage):
    user_id = callback_data.telegram_id
    book_id = callback_data.books

    messages = get_mylikes_api(user_id=user_id)

    if messages['status'] == 'success':
        for message in messages['like_book']:
            if message['telegram_id'] == user_id and message['books'] == book_id:
                add_like = put_book_details_api(pk=book_id, number=-1)
                dislike = delete_mylikes_api(pk=message['id'])
    
    await bot.answer_callback_query(call.id, text='💔Kitob yoqtirilganlar ro\'yxatidan o\'chirildi.', show_alert=False)


async def next_book(call: CallbackQuery, bot: Bot, callback_data: NextLine):
    start_id = callback_data.start_id
    
    books = get_book_search(callback_data.search_name)

    nexts = next_button(books=books, next_id = start_id, types='next', search_name=callback_data.search_name)
    await call.bot.edit_message_reply_markup(chat_id = call.message.chat.id, message_id=call.message.message_id, reply_markup=nexts)

async def next_booklikes(call: CallbackQuery, bot: Bot, callback_data: NextLine):
    start_id = callback_data.start_id
    search_id = callback_data.search_name
    
    books = get_mylikes_api(callback_data.search_name)['like_book']

    nexts = next_like_button(books=books, next_id = start_id, types='next_like', search_name=search_id)
    await call.bot.edit_message_reply_markup(chat_id = call.message.chat.id, message_id=call.message.message_id, reply_markup=nexts)
    # await call.bot.edit_message_text(text="❤️Siz yoqtirgan kitoblar:", chat_id = call.message.chat.id, message_id=call.message.message_id, reply_markup=nexts)


# async def prev_book(call: CallbackQuery, bot: Bot, callback_data: NextLine):
#     start_id = callback_data.start_id
#     books = get_book_search(callback_data.search_name)

#     prev = prev_button(books=books, next_id = start_id, types='prev', search_name=callback_data.search_name)
#     # await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
#     await call.message.reply(text=f"⬇️ Qidiruv natijalari:", reply_markup=prev)

async def update_message(call: CallbackQuery, bot: Bot, state: FSMContext):
    await call.message.answer(text="Sarlavhani kiriting: ", reply_markup=stop_channel())
    await state.set_state(UpdateMessage.title)


async def update_title(message: Message, bot: Bot, state: FSMContext):
    text = message.text
    if text == "Qaytish":
        await state.clear()
        await message.answer(text="To'xtildi✅", reply_markup=ReplyKeyboardRemove())
    else:
        updates = put_message_api(text)
        await state.clear()

        if updates['status'] == "success":
            await message.answer(text="O'zgartirildi", reply_markup=ReplyKeyboardRemove())

async def posted_channel(call: CallbackQuery, bot: Bot, state: FSMContext):
    await call.message.answer(text="Kanal Nomini kiriting: ", reply_markup=stop_channel())
    await state.set_state(ChannelsLink.name)


async def channel_name(message: Message, bot: Bot, state: FSMContext):
    name = message.text

    if name == "Qaytish":
        await state.clear()
        await message.answer(text="To'xtildi✅", reply_markup=ReplyKeyboardRemove())
    else:
        await state.update_data(name=name)
        await message.answer(text="Kanal Linkini kiriting: ", reply_markup=stop_channel())
        await state.set_state(ChannelsLink.link)

async def channel_link(message: Message, bot: Bot, state: FSMContext):
    link = message.text

    if link == "Qaytish":
        await state.clear()
        await message.answer(text="To'xtildi✅", reply_markup=ReplyKeyboardRemove())
    else:
        if link.startswith("https://t.me/"):
            await state.update_data(link=link)
            data = await state.get_data()
            resault = post_chennel_api(name=data['name'], link=data['link'])
            await message.answer(text="Kanal muvaffaqiyatli saqlandi ✅")
            await message.answer(text="Botni Kanalga admin qilishni unutmang ❗️", reply_markup=ReplyKeyboardRemove())
            await state.clear()
        else:
            await message.answer(text="Noto'g'ri telegram link kiritdingiz. qaytadan urinib ko'ring: ")
            await state.set_state(ChannelsLink.link)


async def channel_delete(call: CallbackQuery, bot: Bot):
    channel = get_chennel_api()

    keyboards = get_channel_button(btn=channel)
    await call.message.answer(text="O'chirish uchun kanalni tanlang: ", reply_markup=keyboards)

async def channel_edit(call: CallbackQuery, callback_data: DeleteChannel):
    channel_id = callback_data.channel_id
    resaults = delete_channel_api(channel_id)

    channel = get_chennel_api()
    keyboards = get_channel_button(btn=channel)
    
    await call.bot.delete_message(chat_id = call.message.chat.id, message_id=call.message.message_id)
    await call.message.answer("O'chirish uchun kanalni tanlang: ", reply_markup=keyboards)
    
    await call.message.answer('Kanal Muvaffaqiyatli o\'chirildi')
