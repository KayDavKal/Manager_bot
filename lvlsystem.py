import aiosqlite

async def lvlsystem():
    try:
        conn = await aiosqlite.connect('lvlsystem.db')
        c = await conn.cursor()

        await c.execute('''CREATE TABLE IF NOT EXISTS lvlsystem
                           (guild_id TEXT, user_id TEXT, xp TEXT, level TEXT)''')
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

async def add_xp(guild_id, user_id, xp):
    conn = await aiosqlite.connect('lvlsystem.db')
    c = await conn.cursor()

    await c.execute('''SELECT xp FROM lvlsystem WHERE guild_id = ? AND user_id = ?''', (guild_id, user_id))
    result = await c.fetchone()

    if result:
        current_xp = int(result[0])
        new_xp = current_xp + xp
        await c.execute('''UPDATE lvlsystem SET xp = ? WHERE guild_id = ? AND user_id = ?''', (new_xp, guild_id, user_id))
    else:
        level = 0
        await c.execute('''INSERT INTO lvlsystem (guild_id, user_id, level, xp) VALUES (?, ?, ?, ?)''', (guild_id, user_id, level, xp))

    await conn.commit()
    await conn.close()

async def get_level(guild_id, user_id):
  conn = await aiosqlite.connect('lvlsystem.db')
  c = await conn.cursor()

  await c.execute('''SELECT level FROM lvlsystem WHERE guild_id = ? AND user_id = ?''', (guild_id, user_id))
  
  result = await c.fetchone()
  if result:
    level = int(result[0])
    return level
  else:
    return None

  await conn.commit()
  await conn.close()
