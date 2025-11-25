from bot.handlers.handler import Handler, HandlerStatus
import bot.database_client

class DatabaseHandler(Handler):
    def can_handler(self, update: dict) -> bool:
        return True
    
    def handle(self, update: dict) -> bool:
        bot.database_client.persist_updates([update])
        return HandlerStatus.CONTINUE