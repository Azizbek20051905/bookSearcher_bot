from aiogram.filters.callback_data import CallbackData

class BookInfo(CallbackData, prefix='book'):
    file_id: str
    # file_name: str
    file_type: str

class DeleteMessage(CallbackData, prefix='delete'):
    model: str

class LikeMessage(CallbackData, prefix='like'):
    telegram_id: int
    books: int
    model: str

class NextLine(CallbackData, prefix='next'):
    start_id: int
    model: str
    search_name: str

class PreviousLine(CallbackData, prefix='previous'):
    model: str

class DeleteChannel(CallbackData, prefix='delete'):
    channel_id: int
    model: str