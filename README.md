# Task API

A simple CRUD API for managing a to-do list, built with FastAPI as part of the FlyRank Internship — Backend Track, Week 2.

## What this is

A small REST API that lets you create, read, update, and delete tasks. Data is stored in memory (no database yet), so it resets whenever the server restarts.

## How to run it

1. Clone this repo and enter the folder:
```
   git clone https://github.com/Habibahesham02/todo-api.git
   cd todo-api
```
2. Create and activate a virtual environment:
```
   python -m venv venv
   venv\Scripts\Activate.ps1
```
3. Install dependencies:
```
   pip install fastapi uvicorn
```
4. Run the server:
```
   uvicorn main:app --reload
```
5. Visit `http://localhost:8000` in your browser, or `http://localhost:8000/docs` for Swagger UI.

## Endpoints

| Method | Path            | Description                          |
|--------|-----------------|----------------------------------------|
| GET    | `/`             | API info                              |
| GET    | `/health`       | Health check                          |
| GET    | `/tasks`        | List all tasks                        |
| GET    | `/tasks/{id}`   | Get a single task (404 if missing)    |
| POST   | `/tasks`        | Create a task (400 if title missing)  |
| PUT    | `/tasks/{id}`   | Update a task (404 if missing)        |
| DELETE | `/tasks/{id}`   | Delete a task (204, 404 if missing)   |

## Example request

```
curl -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d "@task.json"

HTTP/1.1 201 Created
content-type: application/json

{"id":4,"title":"Buy milk","done":false}
```

## Swagger UI

Interactive docs are available at `/docs`. Example of a successful `POST /tasks` request:

![Swagger UI screenshot](screenshots/post.png)
![Swagger UI screenshot](screenshots/post2.png)

## Notes

This project uses in-memory storage — all tasks reset when the server restarts. Persistent storage with a database is planned for Week 3.