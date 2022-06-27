from utils.db_utils.connect_db import cursor, connect


async def create_table():
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL NOT NULL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    xp INT NOT NULL)""")

    connect.commit()


async def add_new_user(id, name):
    cursor.execute(f"""INSERT INTO users VALUES ({id}, '{name}', {0}) ON CONFLICT DO NOTHING""")

    connect.commit()


async def disconnect_db():
    connect.close()