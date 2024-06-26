from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='♻️Botni Yangilash.'
        ),
        BotCommand(
            command='help',
            description='🎛Barcha buyruqlar'
        ),
        BotCommand(
            command='top',
            description='📚Mashhur Kitoblar'
        ),
        BotCommand(
            command='my_like',
            description='❤️Sevimli kitoblar'
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())

async def set_commands_admin(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='♻️Botni Yangilash.'
        ),
        BotCommand(
            command='help',
            description='🎛Barcha buyruqlar'
        ),
        BotCommand(
            command='top',
            description='📚Mashhur Kitoblar'
        ),
        BotCommand(
            command='my_like',
            description='❤️Sevimli kitoblar'
        ),
        BotCommand(
            command='admin_panel',
            description='Admin Panel'
        ),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())