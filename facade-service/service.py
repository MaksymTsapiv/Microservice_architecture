from fastapi import FastAPI
from starlette.status import HTTP_200_OK

from starlette.requests import Request
from starlette.responses import Response
from starlette.testclient import TestClient

import hazelcast

from consul import Consul

import uvicorn
from argparse import ArgumentParser
from uuid import uuid4
import httpx
import json
import os
import random

CONFIG_FILE = f"{os.path.dirname(__file__)}/../config.json"

with open(CONFIG_FILE, 'r') as file:
    config = json.load(file)

parser = ArgumentParser()
parser.add_argument('--port', type=int, required=True)
args = parser.parse_args()
name = f'facade{args.port}'

consul = Consul()
consul.agent.service.register(name=name, port=args.port)

hz = hazelcast.HazelcastClient(cluster_members=[f"localhost:{hport}" for
                                                hport in consul.kv.get('mq_ports')[1]['Value'].decode("utf-8").split()],
                               cluster_name="dev")

queue = hz.get_queue(consul.kv.get('mq_name')[1]['Value'].decode("utf-8")).blocking()

app = FastAPI()

consul = Consul()
consul.agent.service.register(name="facade-service", port=8080)

@app.post("/facade-service", response_class=Response)
async def post_message(request: Request) -> Response:
    logging_url = config['logging-service'][random.randint(0, 2)]

    bmsg = await request.body()
    msg = bmsg.decode('utf-8')

    uuid = str(uuid4())
    httpx.post(logging_url, json={"uuid": uuid, "msg": msg})

    queue.put(msg)

    return Response(status_code=HTTP_200_OK)


@app.get("/facade-service")
def get_message():
    logging_url = config['logging-service'][random.randint(0, 2)]
    messages_url = config['messages-service'][random.randint(0, 1)]
    
    log_response = httpx.get(logging_url)
    msg_response = httpx.get(messages_url)

    return log_response.json(), msg_response.json()


if __name__ == "__main__":
    uvicorn.run("service:app", port=args.port, log_level="info")