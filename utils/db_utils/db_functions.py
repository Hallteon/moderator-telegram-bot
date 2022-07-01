from utils.db_utils.connect_db import cursor, connect


async def create_table():
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(30) NOT NULL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    xp INT NOT NULL,
    mute_time INT NOT NULL)""")

    connect.commit()


async def add_new_user(id, name):
    cursor.execute(f"""INSERT INTO users VALUES ('{id}', '{name}', {0}, {30}) ON CONFLICT DO NOTHING""")
    connect.commit()


async def add_mute_time(id):
    cursor.execute(f"""UPDATE users SET mute_time = mute_time * 2 WHERE id = '{str(id)}';""")
    connect.commit()


async def get_mute_time(id):
    cursor.execute(f"""SELECT mute_time FROM users WHERE id = '{str(id)}';""")

    return int(cursor.fetchone()[0])


async def get_user_id(name):
    cursor.execute(f"""SELECT id FROM users WHERE name = '{name}';""")

    return int(cursor.fetchone()[0])


async def get_user_xp(id):
    cursor.execute(f"""SELECT xp FROM users WHERE id = '{id}';""")

    return cursor.fetchone()[0]


async def add_user_xp(id, xp):
    cursor.execute(f"""UPDATE users SET xp = xp + {xp} WHERE id = '{str(id)}';""")
    connect.commit()


async def remove_user_xp(id, xp):
    cursor.execute(f"""UPDATE users SET xp = xp - {xp} WHERE id = '{str(id)}';""")
    connect.commit()


async def get_all_users():
    cursor.execute("""SELECT name, id FROM users ORDER BY name ASC;""")
    users = {}

    for user in cursor.fetchall():
        name = user[0]
        id = user[1]

        users[name] = int(id)

    return users


async def terminate_user(id):
    cursor.execute(f"""DELETE FROM users WHERE id = '{id}';""")
    connect.commit()


async def disconnect_db():
    connect.close()