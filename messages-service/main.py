from fastapi import FastAPI
from starlette.status import HTTP_200_OK

from starlette.requests import Request
from starlette.responses import Response

import uvicorn
import os
import json

CONFIG_FILE = f"{os.path.dirname(__file__)}/../config.json"

with open(CONFIG_FILE, 'r') as file:
    config = json.load(file)

database = {}

app = FastAPI()

@app.get("/messages-service")
async def get():
    return "Works as intended"



if __name__ == "__main__":
    uvicorn.run("main:app", port=8082, log_level="info")

