import os
import logging
from random import choice
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

logging.basicConfig(level = logging.INFO)
os.chdir(os.path.dirname(os.path.abspath(__file__)))
with open('cats.txt', encoding = 'UTF-8') as f:
    cats = f.read().split()

app = FastAPI()

# class Data(BaseModel):
#     obj: str
#     # smth: int | None # Python 3.10 ?

@app.get('/')
async def root():
    return {'Neko': choice(cats)}

@app.get('/favicon.ico')
async def icon():
    return FileResponse('Kuchizu.ico')

@app.get('/Pico.m4a')
async def icon():
    return FileResponse('Boku no pico.m4a')
