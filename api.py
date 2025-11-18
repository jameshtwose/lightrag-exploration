from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import logging

# local imports
from routers import rag_router, frontend_router, text_router

logging.basicConfig(level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.INFO)
logger = logging.getLogger(__name__)

templates = Jinja2Templates(directory="templates")

app = FastAPI(
    title="campaign-generator-api",
    version="0.0.1",
    description="General API for the campaign generator.",
    contact={
        "email": "contact@jamestwose.com",
    }
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(frontend_router.router)
app.include_router(text_router.router)
app.include_router(rag_router.router)

@app.get("/")
async def root():
    return templates.TemplateResponse("home.html", {"request": {}})