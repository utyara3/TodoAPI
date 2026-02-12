import aiosqlite

from config import DB_PATH


async def init_db() -> None:
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                is_completed INTEGER DEFAULT 0 NOT NULL
            )
        """)

        await conn.commit()


async def get_todos() -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as conn:
        conn.row_factory = aiosqlite.Row
        cursor = await conn.execute("SELECT * FROM todos")
        rows = await cursor.fetchall()

        return [dict(row) for row in rows]


async def get_todo_by_id(id: int) -> dict:
    async with aiosqlite.connect(DB_PATH) as conn:
        conn.row_factory = aiosqlite.Row
        cursor = await conn.execute("SELECT * FROM todos WHERE id = ?", (id,))
        row = await cursor.fetchone()

        return dict(row) if row else {}


async def create_todo(title: str, description: str) -> int:
    async with aiosqlite.connect(DB_PATH) as conn:
        cursor = await conn.execute(
            """               
            INSERT INTO todos (title, description)
            VALUES (?, ?)
            """,
            (title, description),
        )
        await conn.commit()

        if cursor.lastrowid is None:
            raise RuntimeError("Failed to create todo: lastrowid is None.")

        return cursor.lastrowid


async def update_todo(todo_id: int, data: dict) -> dict:
    sql_query = ", ".join(f"{key} = ?" for key in data.keys())
    values = list(data.values()) + [todo_id]

    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute(
            f"""
            UPDATE todos SET {sql_query} WHERE id = ?
            """,
            values,
        )
        await conn.commit()

    return await get_todo_by_id(todo_id)


async def delete_todo(todo_id: int) -> None:
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))

        await conn.commit()
