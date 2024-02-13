from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from ninja import Schema

class UserCreateRequest(Schema):
    username: str
    email: str
    password: str
    category: str

class UserResponse(Schema):
    id: int
    username: str
    email: str

class ProfileSerializer(Schema):
    user: UserResponse
    category: str

class OrderSerializer(Schema):
    id: int
    title: str
    description: str
    category: str