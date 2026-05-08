from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from database import create_table

app = FastAPI()

create_table()


class Task(BaseModel):
    title: str
    completed: bool = False


def get_connection():
    return sqlite3.connect("tasks.db")


@app.get("/")
def home():
    return {"message": "Task API with SQLite is running!"}


@app.get("/tasks")
def get_tasks():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()

    connection.close()

    tasks = []

    for row in rows:
        tasks.append({
            "id": row[0],
            "title": row[1],
            "completed": bool(row[2])
        })

    return tasks


@app.post("/tasks")
def create_task(task: Task):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO tasks (title, completed) VALUES (?, ?)",
        (task.title, int(task.completed))
    )

    connection.commit()

    new_id = cursor.lastrowid

    connection.close()

    return {
        "id": new_id,
        "title": task.title,
        "completed": task.completed
    }
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    connection.commit()

    deleted = cursor.rowcount

    connection.close()

    if deleted == 0:
        return {"message": "Task not found"}

    return {"message": "Task deleted successfully"}

@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE tasks SET title = ?, completed = ? WHERE id = ?",
        (updated_task.title, int(updated_task.completed), task_id)
    )

    connection.commit()

    updated = cursor.rowcount
    connection.close()

    if updated == 0:
        return {"message": "Task not found"}

    return {
        "id": task_id,
        "title": updated_task.title,
        "completed": updated_task.completed
    }