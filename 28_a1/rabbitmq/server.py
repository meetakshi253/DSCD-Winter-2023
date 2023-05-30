# Assumption: The server does not go offline

import pika
import uuid
import json
from datetime import datetime

SERVERID = str(uuid.uuid1())
MAX_CLIENTS = 10
CLIENTELE = []
ARTICLES = []

serverConnection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost"))
serverChannel = serverConnection.channel()
serverChannel.queue_declare(queue=SERVERID)


class DiscordServer(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost"))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.On_Response,
            auto_ack=True)
        self.response = None
        self.corr_id = None

    def On_Response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def RegisterServer(self):
        print("Attempting to register the server...")
        self.response = None
        self.corr_id = str(uuid.uuid4())
        message = StringifyMessage(
            {"method": "Register", "args": {"servername": SERVERID}})
        self.channel.basic_publish(exchange='', routing_key='registry', properties=pika.BasicProperties(
            reply_to=self.callback_queue,
            correlation_id=self.corr_id,
        ), body=message)
        self.connection.process_data_events(time_limit=None)
        res = ParseJson(self.response)
        print(res["status"])
        return res["status"]


def StringifyMessage(message):
    return json.dumps(message)


def ParseJson(message):
    return json.loads(message)


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


def JoinServer(request):
    print(f'JOIN REQUEST FROM {request["id"]}')
    if len(CLIENTELE) < MAX_CLIENTS and not (request["id"] in CLIENTELE):
        CLIENTELE.append(request["id"])
        return {"status": "SUCCESS"}
    else:
        return {"status": "FAIL"}


def LeaveServer(request):
    print(f'LEAVE REQUEST FROM {request["id"]}')
    try:
        CLIENTELE.remove(request["id"])
        return {"status": "SUCCESS"}
    except:
        return {"status": "FAIL"}


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
        return {"status": "SUCCESS"}
    except:
        return {"status": "FAIL"}


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
        return message
    except:
        return {"status": "FAIL"}


def On_Request(ch, method, props, body):
    message = ParseJson(body)
    res = {"status": "FAIL"}
    if message["method"].lower() == "joinserver":
        res = JoinServer(message["args"])
    elif message["method"].lower() == "leaveserver":
        res = LeaveServer(message["args"])
    elif message["method"].lower() == "publisharticle":
        res = PublishArticle(message["args"])
    elif message["method"].lower() == "getarticles":
        res = GetArticles(message["args"])
    response = StringifyMessage(res)
    ch.basic_publish(exchange='', routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id), body=response)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def Serve():
    # create a server
    serverChannel.basic_qos(prefetch_count=1)
    serverChannel.basic_consume(queue=SERVERID, on_message_callback=On_Request)
    print("Server started")
    serverChannel.start_consuming()


if __name__ == '__main__':
    discord = DiscordServer()
    response = discord.RegisterServer()
    discord.channel.close()
    discord.connection.close()
    if not response.lower() == "success":
        print("Could not register the server. Exiting.")
        exit(1)
    Serve()
