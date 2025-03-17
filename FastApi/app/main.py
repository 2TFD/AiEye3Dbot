from contextlib import asynccontextmanager
from tkinter.font import names

from fastapi.middleware.cors import CORSMiddleware
import ngrok
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, File, UploadFile, HTTPException
from starlette.requests import Request
from starlette.templating import Jinja2Templates
import os
import shutil
import uuid
import aiofiles


NGROK_AUTH_TOKEN = ("2tENDM10PgJfd3yylSiZGdvYMHx_2ajCcwQnZ2A5VJRrjdDYx", "")
NGROK_EDGE = ("NGROK_EDGE", "edge:edghts_")
APPLICATION_PORT = 8000

@asynccontextmanager
async def lifespan(app: FastAPI):
    ngrok.set_auth_token(NGROK_AUTH_TOKEN)
    ngrok.forward(
        addr=APPLICATION_PORT,
        labels=NGROK_EDGE,
        proto="labeled",
    )
    yield
    ngrok.disconnect()

app = FastAPI()

# Директория для хранения моделей
MODEL_DIR = "model"




templates  = Jinja2Templates(directory='html')
app.mount("/model", StaticFiles(directory=MODEL_DIR), name="model")
UPLOAD_DIRECTORY = './model/'


@app.post("/add")
async def upload_file(file: UploadFile = File(...)):
    # Создаем уникальное имя файла на основе UUID и сохраняем оригинальное расширение
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIRECTORY, unique_filename)

    async with aiofiles.open(file_path, "wb") as buffer:
        while content := await file.read(1024):  # Читаем файл по частям
            await buffer.write(content)
    print(unique_filename)
    return {"filename": unique_filename, "path": file_path}



@app.get("/{filename}")
async def root(req: Request,filename: str):
    return templates.TemplateResponse(
        name="index.html",
        context={"request": req, "name": f'../model/{filename}'}
    )

