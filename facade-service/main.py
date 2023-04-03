from fastapi import FastAPI
from starlette.status import HTTP_200_OK

from starlette.requests import Request
from starlette.responses import Response
from starlette.testclient import TestClient

import uvicorn
from uuid import uuid4
import httpx
import json
import os
import random

CONFIG_FILE = f"{os.path.dirname(__file__)}/../config.json"

with open(CONFIG_FILE, 'r') as file:
    config = json.load(file)

messages_url = config['messages-service']

app = FastAPI()

@app.post("/facade-service", response_class=Response)
async def handle_message(request: Request) -> Response:
    logging_url = config['logging-service'][random.randint(0, 2)]

    bmsg = await request.body()
    msg = bmsg.decode('utf-8')

    uuid = str(uuid4())
    httpx.post(logging_url, json={"uuid": uuid, "msg": msg})

    return Response(status_code=HTTP_200_OK)


@app.get("/facade-service")
def get():
    logging_url = config['logging-service'][random.randint(0, 2)]
    
    log_response = httpx.get(logging_url)
    msg_response = httpx.get(messages_url)

    return log_response.json(), msg_response.json()


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, log_level="info")