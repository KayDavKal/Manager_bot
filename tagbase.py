import aiosqlite
import ast

async def tagbase():
    try:
        conn = await aiosqlite.connect('tag.db')
        c = await conn.cursor()

        await c.execute('''CREATE TABLE IF NOT EXISTS tags
                           (guild_id TEXT, tag_name TEXT, tag_content TEXT, user TEXT, strikes TEXT)''')
        await conn.commit()
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        await conn.close()

async def tag_create(guild_id, tag_name, tag_content, user, strikes):
    try:
        conn = await aiosqlite.connect('tag.db')
        c = await conn.cursor()

        await c.execute("SELECT * FROM tags WHERE guild_id = ? AND tag_name = ?", (guild_id, tag_name))
        existing_tag = await c.fetchone()

        if existing_tag is None:
            await c.execute("INSERT INTO tags (guild_id, tag_name, tag_content, user, strikes) VALUES (?, ?, ?, ?, ?)", (guild_id, tag_name, tag_content, user, strikes))
            await conn.commit()
            return True
        else:
            return False
    except Exception as e:
        print(f"Error creating tag: {e}")
    finally:
        await conn.close()

async def tag_check(guild_id, tag_name):
    try:
        conn = await aiosqlite.connect('tag.db')
        c = await conn.cursor()

        await c.execute("SELECT * FROM tags WHERE guild_id = ? AND tag_name = ?", (guild_id, tag_name))
        result = await c.fetchone()
        return result
    except Exception as e:
        print(f"Error checking tag: {e}")
    finally:
        await conn.close()

async def tag_get(guild_id, tag_name):
    try:
        conn = await aiosqlite.connect('tag.db')
        c = await conn.cursor()

        await c.execute("SELECT tag_content FROM tags WHERE guild_id = ? AND tag_name = ?", (guild_id, tag_name))
        result = await c.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"Error getting tag content: {e}")
    finally:
        await conn.close()

async def tag_name(guild_id, tag_name):
    try:
        conn = await aiosqlite.connect('tag.db')
        c = await conn.cursor()

        await c.execute("SELECT user FROM tags WHERE guild_id = ? AND tag_name = ?", (guild_id, tag_name))
        result = await c.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"Error getting tag user: {e}")
    finally:
        await conn.close()

async def add_strike(guild_id, tag_name):
  conn = await aiosqlite.connect('tag.db')
  c = await conn.cursor()
  await c.execute("SELECT strikes FROM tags WHERE guild_id = ? AND tag_name = ?", (guild_id, tag_name))
  strikes_tuple = await c.fetchone()
  if strikes_tuple:
    strikes = int(strikes_tuple[0]) + 1
    await c.execute("UPDATE tags SET strikes = ? WHERE guild_id = ? AND tag_name = ?", (str(strikes), guild_id, tag_name))
  await conn.commit()
  await conn.close()

async def check_strike(guild_id, tag_name):
  conn = await aiosqlite.connect('tag.db')
  c = await conn.cursor()
  await c.execute("SELECT strikes FROM tags WHERE guild_id = ? AND tag_name = ?", (guild_id, tag_name))
  strikes = await c.fetchone()
  await conn.close()
  return strikes[0]

async def del_tag(guild_id, tag_name):
    conn = await aiosqlite.connect('tag.db')
    c = await conn.cursor()
    await c.execute('''DELETE FROM tags WHERE guild_id = ? AND tag_name = ?''', (guild_id, tag_name))
    await conn.commit()
    await conn.close()
