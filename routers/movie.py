from fastapi import FastAPI, Body, Request, HTTPException,Depends, APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional
from user_jwt import createToken,validateToken
from fastapi.security import HTTPBearer
from bd.database import Session,engine,Base
from models.movie import Movie as ModelMovie
from fastapi.encoders import jsonable_encoder

class Movie(BaseModel):
    id: Optional[int]=None
    title:str
    overview:str
    year:int
    rating:float
    category:str

class BearerJWT(HTTPBearer):
    async def __call__(self, request:Request):
        auth= await super().__call__(request)
        data= validateToken(auth.credentials)
        if data ['email']!= 'yerko@gmail.com':
            raise HTTPException(status_code=403, detail='credenciales incorrectas')    


routerMovie=APIRouter()

@routerMovie.get('/movies', tags=['Movies'], dependencies=[Depends(BearerJWT())])
def get_movies():
    db=Session()
    data= db.query(ModelMovie).all()
    return JSONResponse(content=jsonable_encoder(data))

@routerMovie.get('/movies/{id}', tags=['Movies'])
def get_movie(id:int):
    db =Session()
    data=db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        return JSONResponse(status_code=404, content={'message':'Recurso no encontrado'})
    return JSONResponse(status_code=200, content=jsonable_encoder(data))    

@routerMovie.get('/movies/', tags=['Movies'])
def get_movies_by_category(category:str):
    db=Session()
    data=db.query(ModelMovie).filter(ModelMovie.category==category).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(data))

@routerMovie.post('/movies', tags=['Movies'])
def create_movie(movie:Movie):
    db= Session()
    newMovie = ModelMovie(**movie.model_dump())
    db.add(newMovie)
    db.commit()
    return JSONResponse(status_code=201,content={'message':'Se ha creado recurso', 'pelicula':movie.model_dump()})##'pelicula':jsonable_encoder(db.query(ModelMovie).all())

@routerMovie.put('/movies/{id}',tags=['Movies'])
def update_movie(id:int, movie:Movie):
    db=Session()
    data=db.query(ModelMovie).filter(ModelMovie.id==id).first()
    if not data:
        return JSONResponse(status_code=404, content={'message':'no se encontro el recurso'})
    data.title = movie.title
    data.overview = movie.overview
    data.year = movie.year
    data.rating = movie.rating
    data.category = movie.category
    db.commit()
    return JSONResponse(status_code=200, content={'message':'Se modifico el recurso'})

@routerMovie.delete('/movies/{id}', tags=['Movies'])
def delete_movie(id:int):
    db=Session()
    data=db.query(ModelMovie).filter(ModelMovie.id==id).first()
    if not data:
        return JSONResponse(status_code=404, content={'message':'no se encontro el recurso'})
    db.delete(data)
    db.commit()

    return JSONResponse(content={'message':'Se ha eliminado una pelicula', 'pelicula':jsonable_encoder(data)})