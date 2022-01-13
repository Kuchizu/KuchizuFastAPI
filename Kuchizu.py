import os
import logging
from random import choice
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse, FileResponse
from starlette.exceptions import HTTPException

logging.basicConfig(level=logging.INFO)
os.chdir(os.path.dirname(os.path.abspath(__file__)))
with open('files/cats.txt', encoding = 'UTF-8') as f:
    cats = f.read().split()

app = FastAPI()

# from pydantic import BaseModel
# class Data(BaseModel):
#     obj: str
#     # smth: int | None # Python 3.10 ?

@app.get('/')
async def root():
    return {'Neko': choice(cats)}

@app.exception_handler(HTTPException)
async def notfound(request, exc):
    return PlainTextResponse(f'404 Not Found.')

@app.get('/favicon.ico')
async def icon():
    return FileResponse('icons/Kuchizu.ico')

@app.get('/files/{file}')
async def get_file(file):
    if os.path.exists(f'files/{file}'):
        return FileResponse(f'files/{file}')
    else:
        return PlainTextResponse('403 Forbidden.')
