from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.api.routers.analyze import router

app = FastAPI(title="Email Classifier")

templates = Jinja2Templates(directory="src/templates")
app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.include_router(router)


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
