from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID, uuid4
from enum import Enum

from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(50)
    password_hash = fields.CharField(128)
    
    @classmethod()
    async def get_user(cls, username):
        return cls.get(username=username)

    def verify_password(self, password):
        return True

User_Pydantic = pydantic_model_creator(User, name='User')
# Things that users have
UserIn_Pydantic = pydantic_model_creator(User, name='UserIn', exclude_readonly=True)
# Things that users can pass as input

# PUT
class UserUpdateRequest(BaseModel):
    """
    Update user class attributes
    """
    first_name: Optional[str]
    last_name: Optional[str]
    middle_name: Optional[str]
    roles: Optional[List[Role]]