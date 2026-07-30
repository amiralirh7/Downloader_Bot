from loguru import logger


logger.add(
    "storage/logs/bot.log",
    rotation="10 MB",
    retention="10 days"
)


def get_logger():
    return logger