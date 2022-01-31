import os
import logging
from random import choice
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse, FileResponse, HTMLResponse
from starlette.exceptions import HTTPException

logging.basicConfig(level=logging.INFO)
os.chdir(os.path.dirname(os.path.abspath(__file__)))
with open('files/Nekos.txt', encoding = 'UTF-8') as f:
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

async def get_files(path, req_url) -> str:
    path = f'files{path}/'
    html = f"Founded {len(next(os.walk(path))[1])} dirs, {len(next(os.walk(path))[2])} files:<br><br>"
    for dirname in filter(lambda xpath: os.path.isdir(path + xpath), os.listdir(path)):
            html += '• <a href=\"{link}\">{title}/</a><br>'.format(
                link = f"{req_url}{'/' if req_url[-1] != '/' else ''}{dirname}",
                title = dirname
            )
    html += '<br>'
    for filename in filter(lambda xpath: os.path.isfile(path + xpath), os.listdir(path)):
            html += '<a href=\"{link}\">{title}</a>  {filesize}<br>'.format(
                link = f"{req_url}{'/' if req_url[-1] != '/' else ''}{filename}",
                title = filename,
                filesize = f'{os.path.getsize(os.path.join(path, filename)) / 1024 / 1024:.2f}MB'
            )
    return html

@app.get('/files{file_path:path}')
async def get_file(file_path: str, request: Request):
    file_path = '' if file_path == '/' else file_path
    if os.path.isdir(f'files/{file_path}'):
        return HTMLResponse(await get_files(file_path, request.url._url))
    else:
        if os.path.exists(f'files/{file_path}'):
            return FileResponse(f'files/{file_path}')
        else:
           return PlainTextResponse('403 Forbidden.')
