from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
CHAT_ID = env.int("CHAT_ID")
ADMINS = env.list("ADMINS")
DB_URI = env.str("DB_URI")