import threading
import zmq
import json
import time

MAXSERVERS = 12
SERVERS = {}
HEARTBEAT_INTERVAL = 5


def Register(request):
    global SERVERS
    print(f"JOIN REQUEST FROM {request['ip']}:{request['port']}")
    try:
        if len(SERVERS) >= MAXSERVERS:
            raise Exception(
                "Capacity reached. No more servers can be added")
        serverstring = f"{request['servername']} - {request['ip']}:{request['port']}"
        if serverstring in SERVERS:
            raise Exception("Duplicate request")
        SERVERS[serverstring] = True
        return json.dumps({"status": "SUCCESS"})
    except:
        return json.dumps({"status": "FAIL"})


def GetServerList(request):
    res = []
    print(f"SERVER LIST REQUEST FROM client {request['id']}")
    for key in SERVERS:
        if SERVERS[key]:
            res.append(key)
    return json.dumps({"status": "SUCCESS", "servers": res})


def ParseMessage(message):  # message is a python dict
    res = json.dumps({"status": "FAIL"})
    if message["method"].lower() == "register":
        res = Register(message["args"])
    elif message["method"].lower() == "getserverlist":
        res = GetServerList(message["args"])
    return res


def Serve():
    port = 5555
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://*:{port}")
    print(f"Server started, listening on {port}")
    while True:
        # wait for request from client
        message = socket.recv()
        res = ParseMessage(message=json.loads(message)).encode('UTF-8')
        socket.send(res)


if __name__ == '__main__':
    Serve()
