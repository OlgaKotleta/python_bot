from bot.handlers.handler import Handler
from bot.handlers.database_handler import DatabaseHandler
from bot.handlers.message_echo import MessageEcho
from bot.handlers.image_echo import ImageEcho

def get_handlers()->list[Handler]:
    return[
        DatabaseHandler(),
        MessageEcho(),
        ImageEcho(),
    ]