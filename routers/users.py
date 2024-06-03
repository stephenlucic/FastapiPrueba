from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, JSONResponse
from user_jwt import createToken,validateToken



login_user= APIRouter()



class User(BaseModel):
    email:str
    password:str



@login_user.post('/login',tags=['authentication'])
def login(user:User):
    if user.email == 'yerko@gmail.com' and user.password == '123':
        token:str=createToken(user.model_dump())
        print(token)
        return JSONResponse(content=token)