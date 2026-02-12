from fastapi import FastAPI, HTTPException
import uvicorn

from contextlib import asynccontextmanager

from schemas import TodoGetSchema, TodoPostSchema, TodoUpdateSchema
import database as db


@asynccontextmanager
async def lifespan(_: FastAPI):
    await db.init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/todos", response_model=list[TodoGetSchema])
async def get_todos():
    todos_raw = await db.get_todos()

    if not todos_raw:
        raise HTTPException(404, "not created yet")

    return todos_raw


@app.get("/todos/{todo_id}", response_model=TodoGetSchema)
async def get_todo(todo_id: int):
    todo = await db.get_todo_by_id(todo_id)

    if not todo:
        raise HTTPException(404, "todo not found")

    return todo


@app.post("/todos", response_model=TodoGetSchema, status_code=201)
async def create_todo(todo: TodoPostSchema):
    title = todo.title
    description = todo.description

    todo_id = await db.create_todo(title=title, description=description)

    return await db.get_todo_by_id(todo_id)


@app.patch("/todos/{todo_id}", response_model=TodoGetSchema)
async def change_todo(
    todo_id: int, todo_update: TodoUpdateSchema
) -> dict[str, str | bool]:
    model_data = todo_update.model_dump(exclude_unset=True)

    updates = {key: value for key, value in model_data.items()}
    if not updates:
        raise HTTPException(400, "wrong data")

    todo = await db.get_todo_by_id(todo_id)
    if not todo:
        raise HTTPException(404, "wrong todo id")

    updated_todo = await db.update_todo(todo_id, updates)

    return updated_todo


@app.delete("/todos/{todo_id}", status_code=204)
async def delete_todo(todo_id: int) -> None:
    await db.delete_todo(todo_id)


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
