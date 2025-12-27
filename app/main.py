from fastapi import FastAPI
from dotenv import load_dotenv
import os
import uvicorn

from app.routes import router
load_dotenv()

app = FastAPI(
    title="Splitwise API",
    description="API for Splitwise application",
    version="1.0.0"
)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)