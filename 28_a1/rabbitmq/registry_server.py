# Assumption: The server does not go offline

import pika
import json

MAXSERVERS = 12
SERVERS = {}

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost"))
channel = connection.channel()
channel.queue_declare(queue="registry")


def StringifyMessage(message):
    return json.dumps(message)


def ParseJson(message):
    return json.loads(message.decode('UTF-8'))


def Register(request):
    global SERVERS
    print(f"JOIN REQUEST FROM {request['servername']}")
    try:
        if len(SERVERS) >= MAXSERVERS:
            raise Exception(
                "Capacity reached. No more servers can be added")
        if request["servername"] in SERVERS:
            raise Exception("Duplicate request")
        SERVERS[request["servername"]] = True
        return {"status": "SUCCESS"}
    except:
        return {"status": "FAIL"}


def GetServerList(request):
    res = []
    print(f"SERVER LIST REQUEST FROM CLIENT {request['id']}")
    for key in SERVERS:
        if SERVERS[key]:
            res.append(key)
    return {"status": "SUCCESS", "servers": res}


def On_Request(ch, method, props, body):
    message = ParseJson(body)
    res = {"status": "FAIL"}
    if message["method"].lower() == "register":
        res = Register(message["args"])
    elif message["method"].lower() == "getserverlist":
        res = GetServerList(message["args"])
    response = StringifyMessage(res)
    ch.basic_publish(exchange='', routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id), body=response)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def Serve():
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue="registry", on_message_callback=On_Request)
    print("Registry server is running")
    channel.start_consuming()


if __name__ == '__main__':
    Serve()
