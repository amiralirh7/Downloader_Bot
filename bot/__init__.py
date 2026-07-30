from aiogram import Dispatcher

from bot.handlers.start_handler import router as start_router
from bot.handlers.profile_handler import router as profile_router
from bot.handlers.download_handler import router as download_router
from bot.handlers.premium_handler import router as premium_router
from bot.handlers.admin_handler import router as admin_router
from bot.handlers.users_handler import router as users_router
from bot.handlers.sponsors_handler import router as sponsors_router
from bot.handlers.force_join_handler import router as force_join_router


def register_routers(dp: Dispatcher):

    dp.include_router(start_router)
    dp.include_router(profile_router)
    dp.include_router(download_router)
    dp.include_router(premium_router)
    dp.include_router(admin_router)
    dp.include_router(users_router)
    dp.include_router(sponsors_router)
    dp.include_router(force_join_router)