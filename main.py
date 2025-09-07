import os
from fastapi import FastAPI
from dotenv import load_dotenv
from routes.file_management import router
import uvicorn

# Initialize the FastAPI application
app = FastAPI()

# Include the router from file_management.py
app.include_router(router)

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
