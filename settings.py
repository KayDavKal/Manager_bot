import aiosqlite

async def database():
    conn = await aiosqlite.connect('settings.db')
    c = await conn.cursor()

    await c.execute('''CREATE TABLE IF NOT EXISTS settings
                       (guild_id TEXT, scam_delete TEXT DEFAULT 'false', verified_role TEXT, counting_channel TEXT)''')
    await conn.commit()
    await conn.close()

async def set_scam_delete(guild_id, scam_delete):
    conn = await aiosqlite.connect('settings.db')
    c = await conn.cursor()

    await c.execute("SELECT * FROM settings WHERE guild_id = ?", (guild_id,))
    result = await c.fetchone()
    if result is None:
        await c.execute("INSERT INTO settings (guild_id, scam_delete) VALUES (?, ?)", (guild_id, scam_delete))
    else:
        await c.execute("UPDATE settings SET scam_delete = ? WHERE guild_id = ?", (scam_delete, guild_id))

    await conn.commit()
    await conn.close()

async def get_scam_delete(guild_id):
    conn = await aiosqlite.connect('settings.db')
    c = await conn.cursor()

    await c.execute("SELECT scam_delete FROM settings WHERE guild_id = ?", (guild_id,))
    result = await c.fetchone()

    await conn.close()

    if result is not None:
        scam_delete = result[0]
        return scam_delete
    return None

async def set_verified_role(guild_id, role_id):
  conn = await aiosqlite.connect('settings.db')
  c = await conn.cursor()

  await c.execute("SELECT * FROM settings WHERE guild_id = ?", (guild_id,))
  result = await c.fetchone()
  if result is None:
      await c.execute("INSERT INTO settings (guild_id, verified_role) VALUES (?, ?)", (guild_id, role_id))
  else:
      await c.execute("UPDATE settings SET verified_role = ? WHERE guild_id = ?", (role_id, guild_id))

  await conn.commit()
  await conn.close()

async def get_verified_role(guild_id):
  conn = await aiosqlite.connect('settings.db')
  c = await conn.cursor()

  await c.execute("SELECT verified_role FROM settings WHERE guild_id = ?", (guild_id,))
  result = await c.fetchone()

  await conn.close()

  if result is not None:
      role_id = result[0]
      return role_id
  return None
