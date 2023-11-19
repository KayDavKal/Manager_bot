import aiosqlite

async def eco_table():
  conn = await aiosqlite.connect('economy.db')
  c = await conn.cursor()
  await c.execute('''CREATE TABLE IF NOT EXISTS economy (
    guild_id TEXT,
    user_id TEXT,
    balance INTEGER,
    bank INTERGER
  )''')
  await conn.commit()
  await conn.close()

async def get_money(guild_id, user_id):
  conn = await aiosqlite.connect('economy.db')
  c = await conn.cursor()

  await c.execute('''SELECT balance FROM economy WHERE guild_id = ? AND user_id = ?''', (guild_id, user_id))
  result = await c.fetchone()
  if result is None:
    await c.execute('''INSERT INTO economy VALUES (?, ?, ?, ?)''', (guild_id, user_id, 0, 0))
  
  await conn.commit()
  await conn.close()
  return result[0]
  
async def add_money(guild_id, user_id, money):
  conn = await aiosqlite.connect('economy.db')
  c = await conn.cursor()
  await c.execute('''SELECT balance FROM economy WHERE guild_id = ? AND user_id = ?''', (guild_id, user_id))
  result = await c.fetchone()
  if result:
    new_balance = result[0] + money
    await c.execute('''UPDATE economy SET balance = ? WHERE guild_id = ? AND user_id = ?''', (new_balance, guild_id, user_id))
  else:
    await c.execute('''INSERT INTO economy (guild_id, user_id, balance, bank) VALUES (?, ?, ?, ?)''', (guild_id, user_id, money, 0))

  await conn.commit()
  await conn.close()
  return new_balance

async def sub_money(guild_id, user_id, money):
  conn = await aiosqlite.connect('economy.db')
  c = await conn.cursor()
  await c.execute('''SELECT balance FROM economy WHERE guild_id = ? AND user_id = ?''', (guild_id, user_id))
  result = await c.fetchone()
  if result:
    new_balance = result[0] - money
    await c.execute('''UPDATE economy SET balance = ? WHERE guild_id = ? AND user_id = ?''', (new_balance, guild_id, user_id))
  else:
    return False

  await conn.commit()
  await conn.close()
  return new_balance

async def get_bank(guild_id, user_id):
  conn = await aiosqlite.connect('economy.db')
  c = await conn.cursor()

  await c.execute('''SELECT bank FROM economy WHERE guild_id = ? AND user_id = ?''', (guild_id, user_id))
  result = await c.fetchone()
  
  await conn.close()
  return result[0]

async def add_bank(guild_id, user_id, money):
  conn = await aiosqlite.connect('economy.db')
  c = await conn.cursor()
  await c.execute('''SELECT bank FROM economy WHERE user_id = ?''', (user_id,))
  result = await c.fetchone()
  if result:
    new_bank = result[0] + money
    await c.execute('''UPDATE economy SET bank = ? WHERE user_id = ?''', (new_bank, user_id))
  else:
    await c.execute('''INSERT INTO economy (guild_id, user_id, balance, bank) VALUES (?, ?, ?, ?)''', (guild_id, user_id, 0, money))

  await conn.commit()
  await conn.close()
  return new_bank

async def sub_bank(guild_id, user_id, money):
  conn = await aiosqlite.connect('economy.db')
  c = await conn.cursor()
  await c.execute('''SELECT bank FROM economy WHERE guild_id = ? AND user_id = ?''', (guild_id, user_id))
  result = await c.fetchone()
  if result:
    new_bank = result[0] - money
    await c.execute('''UPDATE economy SET bank = ? WHERE guild_id = ? AND user_id = ?''', (new_bank, guild_id, user_id))
  else:
    return False

  await conn.commit()
  await conn.close()
  return new_bank
