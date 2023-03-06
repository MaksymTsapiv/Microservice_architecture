from fastapi import FastAPI
from starlette.status import HTTP_200_OK

from starlette.requests import Request
from starlette.responses import Response

import uvicorn
import os
import json

from pydantic import BaseModel

class Message(BaseModel):
    uuid: str
    msg: str


CONFIG_FILE = f"{os.path.dirname(__file__)}/../config.json"

with open(CONFIG_FILE, 'r') as file:
    config = json.load(file)

database = {}

app = FastAPI()

@app.post("/logging-service", response_class=Response)
async def handle_message(request: Message) -> Response:

    database[request.uuid] = request.msg
    print(database)

    return Response(status_code=HTTP_200_OK)


@app.get("/logging-service")
async def get():
    return list(database.values())



if __name__ == "__main__":
    uvicorn.run("main:app", port=8081, log_level="info")

