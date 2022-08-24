from typing import Optional, List
from models import User, Gender, Role
from fastapi import FastAPI
from uuid import UUID, uuid4

app = FastAPI()

db: List[User] = [

    User(id=UUID("00612a3a-efe5-4a54-8ed2-adc59c46bc0a"),
    first_name="Jamila", 
    last_name="Ahmed",
    gender=Gender.female,
    roles=[Role.admin, Role.user]
),

User(id=UUID("7b78a343-e5c2-4d76-86db-0ee48c6b9a49"),
    first_name="Alex",
    last_name="Jones",
    gender=Gender.male,
    roles=[Role.admin, Role.user]
)

]
# GET HTTP Request
@app.get("/")

async def root():
    return {"Hello": "Mundo"}

@app.get('/api/v1/users')
async def fetch_users():
    return db;


@app.post('/api/v1/users')
async def register_user(user: User):
    db.append(user)
    return {'id', user.id}
