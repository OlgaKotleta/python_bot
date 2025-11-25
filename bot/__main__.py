import bot.database_client
import bot.telegram_client
import time

def main() -> None:
    next_update_offset = 0
    
    try:
        while True:
            updates = bot.telegram_client.getUpdates(next_update_offset)
            
            if updates:
                bot.database_client.persist_updates(updates)
                
                for update in updates:
                    next_update_offset = update["update_id"] + 1
                    
                    if "message" in update and "text" in update["message"]:
                        # Явное указание кодировки для кириллицы
                        message_text = update["message"]["text"]
                        chat_id = update["message"]["chat"]["id"]
                        
                        bot.telegram_client.sendMessage(
                            chat_id=chat_id,
                            text=message_text
                        )
                        print(".", end="", flush=True)
                        
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nBot stopped")

if __name__ == "__main__":
    main()