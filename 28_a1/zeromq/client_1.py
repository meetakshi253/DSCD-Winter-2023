import zmq
import json
import uuid

CLIENTNAME = str(uuid.uuid1())
REQUEST_TIMEOUT = 2000  # wait for 2 seconds
JOINEDSERVERS = {}


def GetServerList(socket):
    serverList = {}
    socket.connect("tcp://127.0.0.1:5555")
    message = json.dumps(
        {"args": {"id": CLIENTNAME}, "method": "GetServerList"}).encode('UTF-8')
    socket.send(message, zmq.NOBLOCK)
    if (socket.poll(REQUEST_TIMEOUT) & zmq.POLLIN) != 0:
        res = json.loads(socket.recv().decode('UTF-8'))
        print(res)
        servers = res["servers"]
        for server in servers:
            spl = server.split(":")
            port = spl[-1]
            ip = spl[0].rsplit("-", 1)[-1].strip()
            servername = spl[0].rsplit("-", 1)[0].strip()
            serverList[servername] = (ip, port)
    else:
        print("Registry server seems to be offline. Exiting.")
        exit(1)
    socket.disconnect("tcp://127.0.0.1:5555")
    return serverList


def ConnectToServer(socket):
    global JOINEDSERVERS
    serverList = GetServerList(socket)
    print("List of servers:")
    for servername in serverList:
        print(
            f"{servername} - {serverList[servername][0]}:{serverList[servername][1]}")
    choice = input("\nEnter the name of the server you wish to join: ")
    try:
        CONN = f"tcp://{serverList[choice][0]}:{serverList[choice][1]}"
        print("Attempting to contact the server", CONN)
        socket.connect(CONN)
        message = {"args": {"id": CLIENTNAME}, "method": "JoinServer"}
        socket.send(json.dumps(message).encode('UTF-8'), zmq.NOBLOCK)
        if (socket.poll(REQUEST_TIMEOUT) & zmq.POLLIN) != 0:
            res = json.loads(socket.recv().decode('UTF-8'))
            print(res["status"])
            if (res["status"] == "SUCCESS"):
                JOINEDSERVERS[choice] = CONN
        else:
            print("Server seems to be offline.\nFAIL.")
        socket.disconnect(CONN)
    except:
        print("Could not connect to server.\nFAIL")
        return


def PushArticle(atype, author, content):
    if len(JOINEDSERVERS) == 0:
        print("Join a server first\nFAIL")
        return
    if not atype.lower() in ["sports", "fashion", "politics"] or len(author) == 0 or len(content) == 0:
        print("FAIL")
        return
    article = {"type": atype, "author": author, "content": content[:200]}
    message = {"method": "PublishArticle", "args": {
        "id": CLIENTNAME, "article": article}}
    choice = input(
        f"Which server do you want to publish to? {JOINEDSERVERS} ")
    try:
        CONN = JOINEDSERVERS[choice]
        socket.connect(CONN)
        socket.send(json.dumps(message).encode('UTF-8'), zmq.NOBLOCK)
        if (socket.poll(REQUEST_TIMEOUT) & zmq.POLLIN) != 0:
            res = json.loads(socket.recv().decode('UTF-8'))
            print(res["status"])
        else:
            print("Server seems to be offline.\nFAIL.")
        socket.disconnect(CONN)
    except:
        print("Could not connect to server.\nFAIL")
        return


def RequestArticles(atype, author, date):
    if len(JOINEDSERVERS) == 0:
        print("Join a server first\nFAIL")
        return
    choice = input(
        f"Which server do you want to get articles from? {JOINEDSERVERS} ")
    articleTags = {"type": atype, "author": author, "timestamp": date}
    message = {"method": "GetArticles", "args": {
        "id": CLIENTNAME, "article": articleTags}}
    try:
        CONN = JOINEDSERVERS[choice]
        socket.connect(CONN)
        socket.send(json.dumps(message).encode('UTF-8'), zmq.NOBLOCK)
        if (socket.poll(REQUEST_TIMEOUT) & zmq.POLLIN) != 0:
            res = json.loads(socket.recv().decode('UTF-8'))
            print(res["status"])
            if (res["status"] == "FAIL"):
                return
            articles = res["articles"]
            count = 0
            for article in articles:
                count += 1
                print(f"{count})")
                print(
                    f"{article['type']}\n{article['author']}\n{article['timestamp']}\n{article['content']}\n")
        else:
            print("Server seems to be offline.\nFAIL")
        socket.disconnect(CONN)
    except:
        print("Could not connect to server.\nFAIL")
        return


def LeaveServer(socket):
    if len(JOINEDSERVERS) == 0:
        print("Join a server first\nFAIL")
        return
    choice = input(f"Which server do you want to leave? {JOINEDSERVERS} ")
    try:
        CONN = JOINEDSERVERS[choice]
        message = {"args": {"id": CLIENTNAME}, "method": "LeaveServer"}
        socket.connect(CONN)
        socket.send(json.dumps(message).encode('UTF-8'), zmq.NOBLOCK)
        if (socket.poll(REQUEST_TIMEOUT) & zmq.POLLIN) != 0:
            res = json.loads(socket.recv().decode('UTF-8'))
            print(res["status"])
            if (res["status"].lower() == "success"):
                JOINEDSERVERS.pop(choice)
        else:
            print("Server seems to be offline.\nFAIL.")
        socket.disconnect(CONN)
    except:
        print("Could not connect to server.\nFAIL")
        return


if __name__ == '__main__':
    context = zmq.Context()
    socket = context.socket(zmq.REQ)

    while 1:
        print("\n---- Operations ----\n")
        print("1: Join a server")
        print("2: Publish an article")
        print("3: Get articles")
        print("4: Leave a server")
        print("5: Exit")
        choice = int(input())

        socket.setsockopt(zmq.LINGER, 0)
        socket.close()
        socket = context.socket(zmq.REQ)

        if choice == 1:
            res = ConnectToServer(socket)

        if choice == 2:
            atype = input(
                "Enter the article type (sports/fashion/politics): ")
            author = input("Enter the author name: ")
            content = input(
                "Enter the article content (only 200 characters, rest would be truncated): ")
            PushArticle(atype, author, content)

        if choice == 3:
            print("Enter the tags. Leave a blank if you do not wish to specify.")
            atype = input(
                "Enter the article type (sports/fashion/politics): ")
            author = input("Enter the author name: ")
            date = input("Enter date of publishing (dd/mm/yyyy): ")
            RequestArticles(atype, author, date)

        if choice == 4:
            LeaveServer(socket)

        if choice == 5:
            exit(0)
