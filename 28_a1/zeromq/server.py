from datetime import datetime
import zmq
import json
import uuid

SERVERNAME = str(uuid.uuid1())
MAX_CLIENTS = 10
CLIENTELE = []
ARTICLES = []

def RegisterServer(socket, port):
    message = {}
    print("Attempting to register the server...")
    args = {"servername": SERVERNAME, "ip": "127.0.0.1", "port": port}
    message["method"] = "Register"
    message["args"] = args
    req = json.dumps(message).encode('UTF-8')
    socket.send(req)
    res = socket.recv().decode('UTF-8')
    res = json.loads(res)
    print(res["status"])
    return res


def JoinServer(request):
    print(f'JOIN REQUEST FROM {request["id"]}')
    if len(CLIENTELE) < MAX_CLIENTS and not (request["id"] in CLIENTELE):
        CLIENTELE.append(request["id"])
        return json.dumps({"status": "SUCCESS"})
    else:
        return json.dumps({"status": "FAIL"})


def PublishArticle(request):
    global ARTICLES
    print(f'ARTICLES PUBLISH FROM {request["id"]}')
    try:
        if not request["id"] in CLIENTELE:
            raise Exception("Client is not subscribed to this server")
        if not request["article"] or not request["article"]["type"] or not request["article"]["author"] or not request["article"]["content"]:
            raise Exception("Malformed request")
        request["article"]["timestamp"] = datetime.now().strftime("%d/%m/%Y")
        request["article"]["content"] = request["article"]["content"][:200]
        ARTICLES.append(request["article"])
        return json.dumps({"status": "SUCCESS"})
    except:
        return json.dumps({"status": "FAIL"})


def GetArticles(request):
    global ARTICLES
    print(f'ARTICLES REQUEST FROM {request["id"]}')
    atype = request["article"]["type"] if request["article"]["type"] else "<BLANK>"
    author = request["article"]["author"] if len(
        request["article"]["author"]) > 0 else "<BLANK>"
    date = request["article"]["timestamp"] if len(
        request["article"]["timestamp"]) > 0 else "<BLANK>"
    print(f"FOR {atype}, {author}, {date}")
    resarticles = []

    try:
        if not request["id"] in CLIENTELE:
            raise Exception("Client is not subscribed to this server")
        for article in ARTICLES:
            authorTag = CheckAuthor(
                article["author"], request["article"]["author"])
            typeTag = CheckType(article["type"], request["article"]["type"])
            dateTag = CheckDate(article["timestamp"],
                                request["article"]["timestamp"])
            if authorTag and typeTag and dateTag:
                resarticles.append(article)
        message = {"status": "SUCCESS", "articles": resarticles}
        return json.dumps(message)
    except:
        return json.dumps({"status": "FAIL"})


def LeaveServer(request):
    print(f'LEAVE REQUEST FROM {request["id"]}')
    try:
        CLIENTELE.remove(request["id"])
        return json.dumps({"status": "SUCCESS"})
    except:
        return json.dumps({"status": "FAIL"})


def ParseMessage(message):  # message is a python dict
    res = json.dumps({"status": "FAIL"})
    if message["method"].lower() == "joinserver":
        res = JoinServer(message["args"])
    elif message["method"].lower() == "leaveserver":
        res = LeaveServer(message["args"])
    elif message["method"].lower() == "publisharticle":
        res = PublishArticle(message["args"])
    elif message["method"].lower() == "getarticles":
        res = GetArticles(message["args"])
    return res


def CheckAuthor(aAuthor, rAuthor):
    if len(rAuthor) == 0 or aAuthor.lower() == rAuthor.lower():
        return True
    else:
        return False


def CheckType(aType, rType):
    if len(rType) == 0 or aType.lower() == rType.lower():
        return True
    else:
        return False


def CheckDate(aDate, rDate):
    if not len(rDate) == 0:
        publishDate = datetime.strptime(
            aDate, "%d/%m/%Y")
        requestedDate = datetime.strptime(
            rDate, "%d/%m/%Y")
        if requestedDate < publishDate:
            return True
        else:
            return False
    else:
        return True


def Serve(socket, port):
    print(f"Server started, listening on {port}")
    while True:
        # wait for request from client
        message = socket.recv()
        res = ParseMessage(message=json.loads(message)).encode('UTF-8')
        socket.send(res)


if __name__ == '__main__':
    port = ''
    context = zmq.Context()
    repsocket = context.socket(zmq.REP)
    reqsocket = context.socket(zmq.REQ)
    try:
        port = repsocket.bind_to_random_port(
            'tcp://*', min_port=5600, max_port=6004, max_tries=100)
    except:
        print("Could not bind server to a port")
        repsocket.close()
        reqsocket.close()
        exit(1)

    reqsocket.connect("tcp://localhost:5555")
    res = RegisterServer(reqsocket, port)
    reqsocket.close()
    if not (res["status"].lower() == "success"):
        print("Could not register the server. Exiting.")
        repsocket.close()
        exit(1)

    Serve(repsocket, port)
