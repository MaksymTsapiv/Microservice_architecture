from argparse import ArgumentParser
from fastapi import FastAPI
from starlette.status import HTTP_200_OK

from starlette.requests import Request
from starlette.responses import Response

import hazelcast

from consul import Consul

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

parser = ArgumentParser()
parser.add_argument('--port', type=int, required=True)
args = parser.parse_args()
name = f'logging{args.port}'

consul = Consul()
consul.agent.service.register(name=name, port=args.port)

hz = hazelcast.HazelcastClient(cluster_members=[f"localhost:{hport}" for
                                                hport in consul.kv.get('map_ports')[1]['Value'].decode("utf-8").split()],
                               cluster_name="dev",
                               lifecycle_listeners=[
        lambda state: print("Lifecycle event >>>", state),
    ])

database = hz.get_map("distributed-map").blocking()

@app.post("/logging-service", response_class=Response)
async def handle_message(request: Message) -> Response:

    database.set(request.uuid, request.msg)
    
    print("INFO:\tLogging msg: ", database.get(request.uuid))
    print("INFO:\tMap size:", database.size())

    return Response(status_code=HTTP_200_OK)


@app.get("/logging-service")
async def get():
    return list(database.values())


if __name__ == "__main__":
    uvicorn.run("service:app", port=args.port, log_level="info") 
