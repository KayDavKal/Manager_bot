import aiosqlite

async def tagbase():
    conn = await aiosqlite.connect('tag.db')
    c = await conn.cursor()

    await c.execute('''CREATE TABLE IF NOT EXISTS tags
                       (guild_id TEXT, tag_name TEXT, tag_content TEXT)''')
    await conn.commit()
    await conn.close()

async def tag_create(guild_id, tag_name, tag_content):
    conn = await aiosqlite.connect('tag.db')
    c = await conn.cursor()

    await c.execute("SELECT * FROM tags WHERE guild_id = ?", (guild_id,))
    result = await c.fetchone()
    if result is None:
        await c.execute("INSERT INTO tags (guild_id, tag_name, tag_content) VALUES (?, ?, ?)", (guild_id, tag_name, tag_content))

    await conn.commit()
    await conn.close()
