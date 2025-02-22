import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from db.database import init_db
from app.routers.users import users_router
from app.logger import logging

# Lifespan event for startup & shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Initializing database...")
    await init_db()
    yield
    logging.info("Application shutting down.")


# Initialize FastAPI with lifespan
app = FastAPI(lifespan=lifespan)

# Include Routers
app.include_router(users_router, prefix="/users", tags=["Users"])


# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Health Tracker API. Visit /docs for API documentation."}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
