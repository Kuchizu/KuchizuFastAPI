import os
import logging
from random import choice
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse, FileResponse, HTMLResponse
from starlette.exceptions import HTTPException

logging.basicConfig(level=logging.INFO)
os.chdir(os.path.dirname(os.path.abspath(__file__)))
with open('files/Cats.txt', encoding = 'UTF-8') as f:
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

@app.get('/files')
async def get_files(request: Request):
    html = f"Founded {len(next(os.walk('files'))[2])} files:<br><br>"
    for root, dirs, files in os.walk('files'):
        for filename in files:
            html += '<a href=\"{link}\">{title}</a>  {filesize}<br>'.format(
                link = f'{request.url._url}/{filename}',
                title = filename,
                filesize = f'{os.path.getsize(os.path.join(root, filename)) / 1024 / 1024:.2f}MB'
            )
    return HTMLResponse(html)


@app.get('/files/{file}')
async def get_file(file):
    if os.path.exists(f'files/{file}'):
        return FileResponse(f'files/{file}')
    else:
        return PlainTextResponse('403 Forbidden.')
