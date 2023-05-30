# Assumption: The server does not go offline
# Bonus has been implemented

from concurrent import futures
import logging

import grpc
import uuid
import discord_pb2
import discord_pb2_grpc
import registry_pb2
import registry_pb2_grpc

from datetime import datetime

MAX_CLIENTS = 10
SUBSCRIBEDSERVERS = {}


class Discord(discord_pb2_grpc.DiscordServicer):

    serverId = str(uuid.uuid1())
    clientele = []
    articles = []

    def PingPong(self, request, context):
        return discord_pb2.HealthCheckResponse(servingstatus=True)

    def JoinServer(self, request, context):
        print(f'JOIN REQUEST FROM {request.id}')
        if len(Discord.clientele) < MAX_CLIENTS and not request.id in Discord.clientele:
            Discord.clientele.append(request.id)
            return discord_pb2.ResponseStatus(status="SUCCESS")
        else:
            return discord_pb2.ResponseStatus(status="FAIL")

    def LeaveServer(self, request, context):
        print(f'LEAVE REQUEST FROM {request.id}')
        try:
            Discord.clientele.remove(request.id)
            return discord_pb2.ResponseStatus(status="SUCCESS")
        except:
            return discord_pb2.ResponseStatus(status="FAIL")

    def PublishArticles(self, request, context):
        # check if the client belongs to the clientele
        print(f'ARTICLES PUBLISH FROM {request.PublisherId.id}')
        try:
            if not request.PublisherId.id in Discord.clientele:
                raise Exception("Client is not subscribed to this server")
            request.Timestamp = datetime.now().strftime("%d/%m/%Y")
            Discord.articles.append(request)
            return discord_pb2.ResponseStatus(status="SUCCESS")
        except:
            return discord_pb2.ResponseStatus(status="FAIL")

    def GetArticles(self, request, context):
        print(f'ARTICLES REQUEST FROM {request.PublisherId.id}')
        atype = "SPORTS" if request.SPORTS else (
                "FASHION" if request.FASHION else "POLITICS" if request.POLITICS else "<BLANK>")
        author = request.Author if len(request.Author) > 0 else "<BLANK>"
        date = request.Timestamp if len(request.Timestamp) > 0 else "<BLANK>"
        print(f"FOR {atype}, {author}, {date}")
        otherArticles = GetArticlesFromOtherServers()
        if not request.PublisherId.id in Discord.clientele:
            raise Exception("Client is not subscribed to this server")
        try:
            for article in Discord.articles + otherArticles:
                authorTag = CheckAuthor(article.Author, request.Author)
                typeTag = CheckType(article.SPORTS, request.SPORTS, article.FASHION,
                                    request.FASHION, article.POLITICS, request.POLITICS)
                dateTag = CheckDate(article.Timestamp, request.Timestamp)
                if (authorTag and typeTag and dateTag):
                    yield article
                continue
        except Exception:
            yield discord_pb2.ArticleFormat(status="FAIL")


def CheckAuthor(aAuthor, rAuthor):
    if len(rAuthor) == 0 or aAuthor.lower() == rAuthor.lower():
        return True
    else:
        return False


def CheckType(aSports, rSports, aFashion, rFashion, aPolitics, rPolitics):
    if (not (rSports or rFashion or rPolitics)) or (aSports and rSports) or (aFashion and rFashion) or (aPolitics and rPolitics):
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


def RegisterServer(servername, port):
    print("Attempting to register the server...")
    with grpc.insecure_channel('localhost:50001') as channel:
        stub = registry_pb2_grpc.RegistryStub(channel)
        res = stub.Register(registry_pb2.ServerAddress(
            ServerName=servername, IP="localhost", Port=port))
        print(res)
        return res


def SubscribeToOtherServers():
    global SUBSCRIBEDSERVERS
    print(Discord.serverId)
    while True:
        choice = int(
            input("Enter 1 to subscribe to other servers, 2 to exit\n"))
        if choice == 2:
            break
        elif choice == 1:
            servername = input("Enter server name: ")
            ip = input("Enter ip: ")
            port = input("Enter port: ")
            if servername == Discord.serverId:
                print("Cannot subscribe to itself")
                continue
            try:
                CONN = f"{ip}:{port}"
                with grpc.insecure_channel(CONN) as channel:
                    stub = discord_pb2_grpc.DiscordStub(channel)
                    subs = stub.JoinServer(
                        discord_pb2.ClientIdentifier(id=Discord.serverId))
                    print(subs.status)
                    if subs.status.lower() == "success":
                        SUBSCRIBEDSERVERS[servername] = CONN
            except:
                print("Could not connect to server.")
        continue


def GetArticlesFromOtherServers():
    global SUBSCRIBEDSERVERS
    otherArticles = []
    for server, CONN in SUBSCRIBEDSERVERS.items():
        with grpc.insecure_channel(CONN) as channel:
            stub = discord_pb2_grpc.DiscordStub(channel)
            res = stub.GetArticles(
                discord_pb2.ArticleFormat(Author="", Timestamp="", PublisherId=discord_pb2.ClientIdentifier(id=Discord.serverId)))
            print("Fetching articles from server:", server)
            for i in res:
                if i.status.lower() == "fail":
                    print(i.status)
                    break
                otherArticles.append(i)
    return otherArticles


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    discord_pb2_grpc.add_DiscordServicer_to_server(Discord(), server)
    port = server.add_insecure_port('[::]:0')
    server.start()
    res = RegisterServer(Discord.serverId, port)
    if res.status.lower() == "fail":
        print("Could not register the server. Exiting.")
        exit(1)
    SubscribeToOtherServers()
    print(f"Server started, listening on {port}")
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
