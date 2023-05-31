from datetime import datetime
import sys
import threading
from fastapi import FastAPI
from starlette.status import HTTP_200_OK

from starlette.requests import Request
from starlette.responses import Response

import hazelcast

import uvicorn
import os
import json

CONFIG_FILE = f"{os.path.dirname(__file__)}/../config.json"

with open(CONFIG_FILE, 'r') as file:
    config = json.load(file)

app = FastAPI()

hz = hazelcast.HazelcastClient(cluster_members=["localhost:5701"], cluster_name="dev")
queue = hz.get_queue("mq").blocking()
filename = os.path.join("./data/", f"{datetime.now().isoformat()}.txt")


@app.get("/messages-service")
async def get():    
    with open(filename, 'r') as f:
        return list(map(lambda x: x.strip(), f.readlines()))

def save_msg():
    while True:
        msg = queue.take()
        print(f"INFO:\tMQ receive: {msg}")
        with open(filename, 'a') as f:
            f.write(f"{msg}\n")

@app.on_event('startup')
async def app_startup():
    threading.Thread(target=save_msg, daemon=True).start()


if __name__ == "__main__":
    uvicorn.run("service:app", port=int(f'808{sys.argv[1]}'), log_level="info")

