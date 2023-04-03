from fastapi import FastAPI
from starlette.status import HTTP_200_OK

from starlette.requests import Request
from starlette.responses import Response

import hazelcast

import uvicorn
import os
import json
import sys

from pydantic import BaseModel

class Message(BaseModel):
    uuid: str
    msg: str


CONFIG_FILE = f"{os.path.dirname(__file__)}/../config.json"

with open(CONFIG_FILE, 'r') as file:
    config = json.load(file)

app = FastAPI()

client = hazelcast.HazelcastClient(
    cluster_name="dev",
    cluster_members=[
        "127.0.0.1:5701",
        "127.0.0.1:5702",
        "127.0.0.1:5703",
    ],

    lifecycle_listeners=[
        lambda state: print("Lifecycle event >>>", state),
    ]
)
database = client.get_map("distributed-map").blocking()

@app.post("/logging-service", response_class=Response)
async def handle_message(request: Message) -> Response:

    database.set(request.uuid, request.msg)
    
    print(database.get(request.uuid))
    print("Map size:", database.size())

    return Response(status_code=HTTP_200_OK)


@app.get("/logging-service")
async def get():
    return list(database.values())


if __name__ == "__main__":
    uvicorn.run("main:app", port=int(f'808{sys.argv[1]}'), log_level="info") 
