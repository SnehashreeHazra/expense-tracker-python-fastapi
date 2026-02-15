from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
import json
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Expense Tracker API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage (works instantly)
expenses_file = "expenses.json"


class ExpenseBase(BaseModel):
    title: str
    amount: float
    category: str

class Expense(ExpenseBase):
    id: int
    date: str

@app.get("/")
def root():
    return {"message": "Expense Tracker API - Ready!"}

@app.get("/expenses/", response_model=List[Expense])
def get_expenses():
    if os.path.exists(expenses_file):
        with open(expenses_file, "r") as f:
            return json.load(f)
    return []

@app.post("/expenses/")
def create_expense(expense: ExpenseBase):
    current_expenses = []

    if os.path.exists(expenses_file):
        with open(expenses_file, "r") as f:
            current_expenses = json.load(f)

    new_id = max([e["id"] for e in current_expenses], default=0) + 1

    new_expense = {
        "id": new_id,
        "title": expense.title,
        "amount": expense.amount,
        "category": expense.category,
        "date": datetime.now().isoformat()
    }

    current_expenses.append(new_expense)

    with open(expenses_file, "w") as f:
        json.dump(current_expenses, f)

    return new_expense

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    current_expenses = []

    if os.path.exists(expenses_file):
        with open(expenses_file, "r") as f:
            current_expenses = json.load(f)

    current_expenses = [e for e in current_expenses if e["id"] != expense_id]

    with open(expenses_file, "w") as f:
        json.dump(current_expenses, f)

    return {"message": "Deleted"}
