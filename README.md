## Basic Mircoservices

### Prerequirements
    python 3.6 or higher

> ### Create venv and install requirements.txt
>```bash
>$ python -m venv venv
>
>$ . venv/bin/activate
>
>$ pip install -r requirements.txt 
>
>```
> </>

### Usage

> First run all 3 microservices (use 3 separate terminals):

```
 $ python facade-service/main.py

 $ python logging-service/main.py

 $ python messages-service/main.py
```

> Now you can make POST/GET requests using `curl` for example:

```
 $ curl -X POST http://127.0.0.1:8080/facade-service -H "Content-Type: text/html" -d 'msg1'

 $ curl -X POST http://127.0.0.1:8080/facade-service -H "Content-Type: text/html" -d 'msg2'

 $ curl -X GET http://127.0.0.1:8080/facade-service

```

### Output

> POST requests do not give output. GET requests return messages you posted and a static message from `message-service` (`"Works as intended"`). 

Output example after a GET request:
```
[["msg1","msg2","msg3","msg4"],"Works as intended"]
```

You can also see how `logging-service` is storing your messages with its uuids if you look inside the console output where you started logging service using:

    $ python logging-service/main.py

This is an example:

```
INFO:     Started server process [35546]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8081 (Press CTRL+C to quit)
{'25f4c8eb-5395-48e2-b6d1-8a60bb70e398': 'msg1'}
INFO:     127.0.0.1:45952 - "POST /logging-service HTTP/1.1" 200 OK
{'25f4c8eb-5395-48e2-b6d1-8a60bb70e398': 'msg1', 'c67be0f9-d65b-4433-9153-cad02f5edfca': 'msg2'}
INFO:     127.0.0.1:35966 - "POST /logging-service HTTP/1.1" 200 OK
{'25f4c8eb-5395-48e2-b6d1-8a60bb70e398': 'msg1', 'c67be0f9-d65b-4433-9153-cad02f5edfca': 'msg2', '4766d0a9-ca2c-4a2a-9c99-8ad206542bed': 'msg3'}
INFO:     127.0.0.1:35112 - "POST /logging-service HTTP/1.1" 200 OK
INFO:     127.0.0.1:51860 - "GET /logging-service HTTP/1.1" 200 OK
{'25f4c8eb-5395-48e2-b6d1-8a60bb70e398': 'msg1', 'c67be0f9-d65b-4433-9153-cad02f5edfca': 'msg2', '4766d0a9-ca2c-4a2a-9c99-8ad206542bed': 'msg3', 'f7e9b409-ecae-4667-b3bf-fc46200336e2': 'msg4'}
INFO:     127.0.0.1:43832 - "POST /logging-service HTTP/1.1" 200 OK
INFO:     127.0.0.1:43836 - "GET /logging-service HTTP/1.1" 200 OK
```
