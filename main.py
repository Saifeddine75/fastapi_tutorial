# Packages
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from uuid import UUID, uuid4
from typing import Optional, List

from tortoise.contrib.fastapi import register_tortoise
from models import User, Gender, Role, UserUpdateRequest

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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

# Authentification
@app.post('/token')
# Depends means return can be a form or nothing
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    return {'access_token': form_data.username + 'token'}

@app.get("/")
async def index(token: str = Depends(oauth2_scheme)):
    return {'the_token': token}

@app.get('/api/v1/users')
async def fetch_users():
    return db;

@app.post('/api/v1/users')
async def register_user(user: User):
    db.append(user)
    return {'id', user.id}

@app.delete('/api/v1/users/{user_id}')
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return
    
    raise HTTPException(
        status_code=404,
        detail=f'user with id: "{user_id}" does not exists'
    )

@app.put("/api/v1/users/{user_id}")
async def update_user(user_update: UserUpdateRequest, user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name
            if user_update.roles is not None:
                user.roles = user_update.roles 
            return
    
    raise HTTPException(
        status_code=404,
        detail=f'user with id "{user_id}" does not exists'
    )


register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['models']},
    generate_schemas=True,  # Create Table if it not exist
    add_exception_handlers=True,
)
