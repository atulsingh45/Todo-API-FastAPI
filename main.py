from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional, List
from models import TodoModel
from database import SessionLocal, Base, engine

app = FastAPI()  # Create FastAPI instance

# Create tables in the database
Base.metadata.create_all(bind=engine)

# Pydantic schema base class for shared fields
class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

# Schema for creating todos
class TodoCreate(TodoBase):
    pass

# Schema for updating todos
class TodoUpdate(TodoBase):
    pass

# Response schema including the id for ORM mode
class TodoResponse(TodoBase):
    id: int
    class Config:
        orm_mode = True

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Route to get all todos
@app.get("/todos", response_model=List[TodoResponse])
def get_todos(db: Session = Depends(get_db)):
    todos = db.query(TodoModel).all()
    return todos

# Route to get a single todo by id
@app.get("/todos/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id)
    return todo.first()

# Route to create a new todo
@app.post("/todos", response_model=TodoResponse)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    todo_model = TodoModel(title=todo.title, description=todo.description, completed=todo.completed)
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    return todo_model

# Route to delete a todo by id
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    db.delete(todo)
    db.commit()
    return todo
