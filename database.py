import aiosqlite
import asyncio
from watchfiles import awatch



async def add_to_database_users(telegram_id, username, tokens):
    async with aiosqlite.connect('users.db') as db:
        await db.execute("CREATE TABLE IF NOT EXISTS users (telegram_id BIGINT, username TEXT, tokens BIGINT)")
        async with db.execute(f'SELECT telegram_id FROM users WHERE telegram_id = ?', (telegram_id,)) as cursor:
            res = await cursor.fetchall()
            nol = []
            if res == nol:
                await db.execute("INSERT INTO users (telegram_id, username, tokens) VALUES(?, ?, ?)",
                                 (telegram_id, username, tokens))
        await db.commit()

async def add_to_database_settings(priceT, startT, priceG, ID):
    async with aiosqlite.connect('settings.db') as db:
        await db.execute("CREATE TABLE IF NOT EXISTS settings (priceT BIGINT, startT BIGINT, priceG BIGINT, ID BIGINT)")
        await db.execute("INSERT INTO settings (priceT, startT, priceG, ID) VALUES(?, ?, ?, ?)",
                         (priceT, startT, priceG, ID))
        await db.commit()


async def add_pricet(priceT):
    async with aiosqlite.connect('settings.db') as db:
        async with db.execute(f'UPDATE settings SET priceT = ? WHERE ID = 1',(priceT,)):
            await db.commit()

async def add_startt(startT):
    async with aiosqlite.connect('settings.db') as db:
        async with db.execute(f'UPDATE settings SET startT = ? WHERE ID = 1',(startT,)):
            await db.commit()

async def add_priceg(priceG):
    async with aiosqlite.connect('settings.db') as db:
        async with db.execute(f'UPDATE settings SET priceG = ? WHERE ID = 1',(priceG,)):
            await db.commit()


async def get_tokens(id):
    async with aiosqlite.connect('users.db') as db:
        async with db.execute(f'SELECT tokens FROM users WHERE telegram_id = ?',(id,)) as cur:
            res = await cur.fetchall()
            return res[0][0]


async def get_Start_tokens():
    async with aiosqlite.connect('settings.db') as db:
        async with db.execute(f'SELECT startT FROM settings WHERE ID = 1', ()) as cur:
            res = await cur.fetchall()
            return res[0][0]


async def add100tokens(ID):
    async with aiosqlite.connect('users.db') as db:
        user_tokens = await get_tokens(ID)
        new_tokens = user_tokens + 100
        async with db.execute(f'UPDATE users SET tokens = ? WHERE telegram_id = ?',(new_tokens, ID)):
            await db.commit()
async def add500tokens(ID):
    async with aiosqlite.connect('users.db') as db:
        user_tokens = await get_tokens(ID)
        new_tokens = user_tokens + 500
        async with db.execute(f'UPDATE users SET tokens = ? WHERE telegram_id = ?',(new_tokens, ID)):
            await db.commit()
async def add1000tokens(ID):
    async with aiosqlite.connect('users.db') as db:
        user_tokens = await get_tokens(ID)
        new_tokens = user_tokens + 1000
        async with db.execute(f'UPDATE users SET tokens = ? WHERE telegram_id = ?',(new_tokens, ID)):
            await db.commit()


async def get_price100():
    async with aiosqlite.connect('settings.db') as db:
        async with db.execute(f'SELECT priceT FROM settings WHERE ID = 1', ()) as cur:
            res = await cur.fetchall()
            return res[0][0]

async def get_pricegen():
    async with aiosqlite.connect('settings.db') as db:
        async with db.execute(f'SELECT priceG FROM settings WHERE ID = 1', ()) as cur:
            res = await cur.fetchall()
            return res[0][0]

async def buygen(ID):
    async with aiosqlite.connect('users.db') as db:
        user_tokens = await get_tokens(ID)
        priceT = await get_pricegen()
        new_tokens = user_tokens - priceT
        async with db.execute(f'UPDATE users SET tokens = ? WHERE telegram_id = ?',(new_tokens, ID)):
            await db.commit()