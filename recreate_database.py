import bot.database_client

if __name__ == "__main__":
    bot.database_client.recreate_database()
    print("Database created successfully")