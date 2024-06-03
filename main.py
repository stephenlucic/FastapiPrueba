from fastapi import FastAPI, Body, Request, HTTPException,Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional
from user_jwt import createToken,validateToken
from fastapi.security import HTTPBearer
from bd.database import Session,engine,Base
from models.movie import Movie as ModelMovie
from fastapi.encoders import jsonable_encoder
from routers.movie import routerMovie
from routers.users import login_user

app=FastAPI(
    title='Aprendiendo FastApi',
    description='una api en los primeros pasos',
    version='0.0.1'
)

app.include_router(routerMovie)
app.include_router(login_user)

Base.metadata.create_all(bind=engine)



##movies=[
##    {
##        'id':1,
##        'title':'El Padrino',
##        'overview':"El padrino es una película de 1972 dirigida por Francis Ford Coppola ...",
##        'year':'1972',
##        'rating':9.2,
##        'category':'crimen'
##    }
##]


@app.get('/', tags=['inicio'])
def read_root():
    return HTMLResponse('<h2>Hola mundo!</h2>')

