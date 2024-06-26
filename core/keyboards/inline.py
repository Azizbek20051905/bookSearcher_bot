from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from core.utils.callbackdata import BookInfo, PreviousLine, DeleteMessage, LikeMessage, NextLine, DeleteChannel
from core.db_api.DB import get_chennel_api, get_book_details_api
from core.settings import settings

def get_channel_keyboard():
    channel_inline_keyboard = InlineKeyboardBuilder()
    
    channels = get_chennel_api()
    if channels:
        for channel in channels:
            channel_inline_keyboard.button(text=f"{channel['name']}", url=f"{channel['link']}")

    channel_inline_keyboard.button(text="Tasdiqlash✅", url='https://t.me/Xudoyorxon_kitoblari_bot?start=start', callback_data=DeleteMessage(model='delete'))
    # channel_inline_keyboard.button(text="Tasdiqlash✔", callback_data=DeleteMessage(model='delete'))
    channel_inline_keyboard.adjust(1)
    return channel_inline_keyboard.as_markup()


def get_inline_keyboard(books, user_id, searches):
    keyboard_builder = InlineKeyboardBuilder()

    number = 0
    one = 10
    start = 0
    end = 0
    for book in books:
        number += 1

        file_id=int(book['id'])
        file_name=str(book['name'])
        types=str(book['file_type'])

        keyboard_builder.button(text=f"{number}. {book['name']}", callback_data=BookInfo(file_id=str(file_id), file_type=types))
        start=int(file_id)
        if number == 10 or len(books) == number:
            start = file_id
            break
            
    keyboard_builder.button(text="❌", callback_data=DeleteMessage(model="delete"))
    keyboard_builder.adjust(1)
    keyboard_builder.button(text="⏩", callback_data=NextLine(start_id=start, model='next', search_name = searches))
    # keyboard_builder.adjust(3)
    return keyboard_builder.as_markup()

def next_button(books, next_id, types, search_name):
    keyboards = InlineKeyboardBuilder()
    
    number = 0
    start = 0
    nums = 0
    for book in books:
        nums +=1
        file_id=int(book['id'])
        file_name=str(book['name'])
        types=str(book['file_type'])
        if next_id < file_id:
            if book:
                keyboards.button(text=f"{number}. {file_name}", callback_data=BookInfo(file_id=str(file_id), file_type=types))
                start=int(file_id)
                number += 1
                if number == 10 or len(books) == nums:
                    start = file_id
                    break
        
        elif len(books) == nums and file_id == books[nums - 1]['id']:
            for book in books:
                number += 1

                file_id=int(book['id'])
                file_name=str(book['name'])
                types=str(book['file_type'])
                
                keyboards.button(text=f"{number}. {book['name']}", callback_data=BookInfo(file_id=str(file_id), file_type=types))
                start=int(file_id)
                if number == 10 or len(books) == number:
                    start = file_id
                    break
            break

    keyboards.button(text="❌", callback_data=DeleteMessage(model="delete"))
    keyboards.adjust(1)
    keyboards.button(text="⏩", callback_data=NextLine(start_id=start, model='next', search_name=search_name))
    return keyboards.as_markup()

# def prev_button(books, next_id, types, search_name):
#     keyboards = InlineKeyboardBuilder()
    
#     number = 0
#     nums = 0
#     start = 0
#     booklist = []
#     books = books[::-1]

#     for book in books:
#         nums+=1
#         file_id=int(book['id'])
#         if next_id > file_id:
#             booklist.append(book)

#             number += 1
#             if number == 10 or len(books) == nums:
#                 start = file_id
#                 break
    
#     booklist = booklist[::-1]
#     number = 0
#     for book in booklist:
#         number += 1
#         file_id=int(book['id'])
#         file_name=str(book['name'])
#         types=str(book['file_type'])
#         keyboards.button(text=f"{number}. {file_name}", callback_data=BookInfo(file_id=str(file_id), file_type=types))

#     keyboards.button(text="⏪", callback_data=NextLine(start_id=start, model='prev', search_name=search_name))
#     keyboards.adjust(1)
#     keyboards.button(text="❌", callback_data=DeleteMessage(model="delete"))
#     keyboards.button(text="⏩", callback_data=NextLine(start_id=start, model='next', search_name=search_name))
#     return keyboards.as_markup()

def likes(tg_id, book_id):
    like_btn = InlineKeyboardBuilder()
    like_btn.button(text="❤️", callback_data=LikeMessage(telegram_id=tg_id, books=book_id, model='like'))
    like_btn.button(text="❌", callback_data=DeleteMessage(model='delete'))
    like_btn.button(text="💔", callback_data=LikeMessage(telegram_id=tg_id, books=book_id, model='dislike'))
    like_btn.adjust(3)
    return like_btn.as_markup()

def top_inline_keyboard(data):
    keyboard = InlineKeyboardBuilder()
    number = 0

    for book in data['book']:
        number += 1
        file_id=str(book['id'])
        types=str(book['file_type'])

        keyboard.button(text=f"{number}. {book['name']}", callback_data=BookInfo(file_id=file_id, file_type=types))
    
    keyboard.button(text="❌", callback_data=DeleteMessage(model="delete"))
    keyboard.adjust(1)
    return keyboard.as_markup()

def like_inline_keyboard(user_id, books):
    keyboard = InlineKeyboardBuilder()
    number = 0
    start = 0
    for book in books:
        number += 1
        book_id = book['id']

        book = get_book_details_api(pk=book["books"])
        file_id = book['book']["id"]
        types = book['book']["file_type"]
        name = book['book']["name"]


        keyboard.button(text=f"{number}. {name}", callback_data=BookInfo(file_id=str(file_id), file_type=types))
        start=int(book_id)
        if number == 10 or len(books) == number:
            start = int(book_id)
            break
    
    keyboard.button(text="❌", callback_data=DeleteMessage(model="delete"))
    keyboard.adjust(1)
    keyboard.button(text="⏩", callback_data=NextLine(start_id=start, model='next_like', search_name=str(user_id)))
    return keyboard.as_markup()

def next_like_button(books, next_id, types, search_name):
    keyboards = InlineKeyboardBuilder()
    
    number = 0
    start = 0
    nums = 0
    for book in books:
        nums +=1
        book_id = book['id']

        book = get_book_details_api(pk=book["books"])['book']
        file_id=int(book['id'])
        file_name=str(book['name'])
        types=str(book['file_type'])
        if next_id < book_id:
            print()
            print('boshida')
            print()
            if book:
                keyboards.button(text=f"{number}. {file_name}", callback_data=BookInfo(file_id=str(file_id), file_type=types))
                number += 1
                start=int(book_id)
                if number == 10 or len(books) == nums:
                    break
        
        elif len(books) == nums and book_id == books[nums - 1]['id']:
            start = 0
            for book in books:
                number += 1

                book_id = book['id']
                book = get_book_details_api(pk=book["books"])['book']
                
                keyboards.button(text=f"{number}. {book['name']}", callback_data=BookInfo(file_id=str(book['id']), file_type=str(book['file_type'])))
                if number == 10 or len(books) == number:
                    start=int(book_id)
                    break
            break

    keyboards.button(text="❌", callback_data=DeleteMessage(model="delete"))
    keyboards.adjust(1)
    keyboards.button(text="⏩", callback_data=NextLine(start_id=start, model='next_like', search_name=search_name))
    return keyboards.as_markup()

def admin_btn():
    keyboards = InlineKeyboardBuilder()

    keyboards.button(text="📝Sarlavhani o'zgartirish", callback_data=PreviousLine(model="messages"))
    keyboards.button(text="📢Kanal qo'shish", callback_data=PreviousLine(model="add_channel"))
    keyboards.button(text="❌Kanal o'chirish", callback_data=PreviousLine(model="delete_channel"))
    keyboards.button(text="❌", callback_data=DeleteMessage(model="delete"))
    keyboards.adjust(2,1)
    return keyboards.as_markup()

def stop_channel():
    keyboards = ReplyKeyboardBuilder()

    keyboards.button(text="Qaytish")
    keyboards.adjust(1)
    return keyboards.as_markup(resize_keyboard=True)

def get_channel_button(btn):
    keyboards = InlineKeyboardBuilder()

    for button in btn:
        keyboards.button(text=button['name'], callback_data=DeleteChannel(channel_id=int(button['id']), model='delete_channel_entry'))
    
    keyboards.button(text="❌", callback_data=DeleteMessage(model="delete"))
    keyboards.adjust(1)
    return keyboards.as_markup()

