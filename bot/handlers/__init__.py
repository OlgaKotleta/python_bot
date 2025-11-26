from bot.handlers.handler import Handler
from bot.handlers.database_handler import DatabaseHandler
#from bot.handlers.message_echo import MessageEcho
#from bot.handlers.image_echo import ImageEcho
from bot.handlers.ensure_users_exists import EnsureUserExists
from bot.handlers.message_start import MessageStart

def get_handlers()->list[Handler]:
    return[
        DatabaseHandler(),
        EnsureUserExists(),
        #MessageEcho(),
        #ImageEcho(),
        MessageStart(),
    ]