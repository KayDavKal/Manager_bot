import aiosqlite

async def lvlsystem():
    try:
        conn = await aiosqlite.connect('lvlsystem.db')
        c = await conn.cursor()

        await c.execute('''CREATE TABLE IF NOT EXISTS lvlsystem
                           (guild_id TEXT, user TEXT, level TEXT, xp TEXT)''')
        await conn.commit()
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        await conn.close()

async def get_xp(guild_id, user_id):
    conn = await aiosqlite.connect('lvlsystem.db')
    c = await conn.cursor()

    await c.execute('''SELECT xp FROM lvlsystem WHERE guild_id = ? AND user_id = ?''', (guild_id, user_id))
    result = await c.fetchone()

    await conn.commit()
    await conn.close()

    return result
