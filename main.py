import uvicorn
from fastapi import FastAPI
from backend.mongoDB.db_connection import establish_connection
from backend.routes.user_routes import get_user_router

users_collection = None
tokens_collection = None

app = FastAPI()
app.title = "API workout with  pose detection"
app.version = "0.0.1"


def start_application():
    global users_collection, tokens_collection
    users_collection, tokens_collection = establish_connection()
    app.include_router(get_user_router(users_collection, tokens_collection), prefix="/api", tags=["user"])


if __name__ == "__main__":
    start_application()
    uvicorn.run(app, host="localhost", port=8000)
