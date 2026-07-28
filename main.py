from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import sqlite3

app = FastAPI(title="Task API", version="1.0")

DB_FILE = "tasks.db"

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER NOT NULL DEFAULT 0
        )
    """)
    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.executemany(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            [
                ("Buy milk", 0),
                ("Walk the dog", 1),
                ("Finish assignment", 0),
            ]
        )
        conn.commit()

    conn.close()

init_db()

class TaskCreate(BaseModel):
    title: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

def row_to_task(row):
    """Convert a database row into a plain dict, converting 0/1 to bool."""
    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"])
    }

@app.get("/", summary="API info", description="Returns basic info about this API.")
def read_root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }

@app.get("/health", summary="Health check", description="Confirms the server is alive.")
def health_check():
    return {"status": "ok"}

@app.get("/tasks", summary="List all tasks", description="Returns every task in the database.")
def get_tasks():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return [row_to_task(row) for row in rows]

@app.get("/tasks/{task_id}", summary="Get one task", description="Returns a single task by id, or 404 if it doesn't exist.")
def get_task(task_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return row_to_task(row)

@app.post("/tasks", status_code=201, summary="Create a task", description="Creates a new task. Title is required.")
def create_task(task: TaskCreate):
    if not task.title or not task.title.strip():
        raise HTTPException(status_code=400, detail="Title is required")

    # Still using the in-memory list for now — Stage 2 will change this
    next_id = 0  # placeholder, will be replaced in Stage 2
    new_task = {"id": next_id, "title": task.title, "done": False}
    return new_task

@app.put("/tasks/{task_id}", summary="Update a task", description="Updates a task's title and/or done status. 404 if id doesn't exist.")
def update_task(task_id: int, update: TaskUpdate):
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@app.delete("/tasks/{task_id}", status_code=204, summary="Delete a task", description="Removes a task by id. 404 if it doesn't exist.")
def delete_task(task_id: int):
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")