from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.Books.router import book_router
from contextlib import asynccontextmanager
from beanie import init_beanie
from Utils.constans import constants
from motor.motor_asyncio import AsyncIOMotorClient
from src.Books.schemas import Book
import os


@asynccontextmanager
async def lifespan(app: FastAPI):

    client = AsyncIOMotorClient(os.getenv("DB_CONNECTION_URI"))
    database = client[constants["db_name"]]
    # Initialize beanie with the Book document class
    await init_beanie(database=database, document_models=[Book])
    yield
    # Close the connection to MongoDB
    client.close()


app = FastAPI(
    lifespan=lifespan,
    version=constants["api_version"],
    title="Books API",
    description="Books API documentation",
)

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return JSONResponse(
        content={"message": "Redirecting to /"},
        status_code=302,
        headers={"Location": "/docs"},
    )


app.include_router(
    router=book_router, prefix=f"/{constants['api_version']}/books", tags=["Books"]
)
