# Bonus has been implemented

import grpc
import uuid
import logging
import discord_pb2
import discord_pb2_grpc
import registry_pb2
import registry_pb2_grpc

CLIENT_ID = str(uuid.uuid1())
CONN = ""
JOINEDSERVERS = {}


def GetServerList():
    serverList = {}
    with grpc.insecure_channel('localhost:50001') as channel:
        stub = registry_pb2_grpc.RegistryStub(channel)
        servers = stub.GetServerList(registry_pb2.EnquireServers())
        for server in servers:
            spl = server.Server.split(":")
            port = spl[-1]
            ip = spl[0].rsplit("-", 1)[-1].strip()
            servername = spl[0].rsplit("-", 1)[0].strip()
            serverList[servername] = (ip, port)
    return serverList


def CreateArticle(atype, author, content):
    article = discord_pb2.ArticleFormat(
        PublisherId=discord_pb2.ClientIdentifier(id=CLIENT_ID))
    article.Author = author
    article.Content = content[:200]
    if atype.lower() == "sports":
        article.SPORTS = True
    elif atype.lower() == "fashion":
        article.FASHION = True
    elif atype.lower() == "politics":
        article.POLITICS = True
    return article


def ConnectToServer():
    global JOINEDSERVERS
    serverList = GetServerList()
    print("List of servers:")
    for servername in serverList:
        print(
            f"{servername} - {serverList[servername][0]}:{serverList[servername][1]}")
    choice = input("\nEnter the name of the server you wish to join: ")
    print("Attempting to contact the server")
    try:
        CONN = f"{serverList[choice][0]}:{serverList[choice][1]}"
        with grpc.insecure_channel(CONN) as channel:
            stub = discord_pb2_grpc.DiscordStub(channel)
            subs = stub.JoinServer(discord_pb2.ClientIdentifier(id=CLIENT_ID))
            print(subs.status)
            if subs.status.lower() == "success":
                JOINEDSERVERS[choice] = CONN
    except:
        print("Could not connect to server.")
        return


def LeaveServer():
    if len(JOINEDSERVERS) == 0:
        print("Join a server first\nFAIL")
        return
    choice = input(f"Which server do you want to leave? {JOINEDSERVERS} ")
    try:
        CONN = JOINEDSERVERS[choice]
        with grpc.insecure_channel(CONN) as channel:
            stub = discord_pb2_grpc.DiscordStub(channel)
            subs = stub.LeaveServer(discord_pb2.ClientIdentifier(id=CLIENT_ID))
            print(subs.status)
            if subs.status.lower() == "success":
                JOINEDSERVERS.pop(choice)
    except:
        print("Could not connect to server.")
        return


def PushArticle(atype, author, content):
    if len(JOINEDSERVERS) == 0:
        print("Join a server first\nFAIL")
        return
    if not atype.lower() in ["sports", "fashion", "politics"] or len(author) == 0 or len(content) == 0:
        print("FAIL")
        return
    article = CreateArticle(atype, author, content[:200])
    choice = input(
        f"Which server do you want to publish to? {JOINEDSERVERS} ")
    try:
        CONN = JOINEDSERVERS[choice]
        with grpc.insecure_channel(CONN) as channel:
            stub = discord_pb2_grpc.DiscordStub(channel)
            res = stub.PublishArticles(article)
            print(res.status)
    except:
        print("Could not connect to server.")
        return


def RequestArticles(atype, author, date):
    if len(JOINEDSERVERS) == 0:
        print("Join a server first\nFAIL")
        return
    if len(atype) != 0 and not atype.lower() in ["sports", "fashion", "politics"]:
        print("FAIL")
        return
    choice = input(
        f"Which server do you want to get articles from? {JOINEDSERVERS} ")
    articleTags = CreateArticle(atype, author, "")
    articleTags.Timestamp = date
    try:
        CONN = JOINEDSERVERS[choice]
        with grpc.insecure_channel(CONN) as channel:
            stub = discord_pb2_grpc.DiscordStub(channel)
            res = stub.GetArticles(articleTags)
            count = 0
            for i in res:
                if i.status.lower() == "fail":
                    print(i.status)
                    break
                count += 1
                atype = "SPORTS" if i.SPORTS else (
                    "FASHION" if i.FASHION else "POLITICS")
                print(f"{count})")
                print(
                    f"{atype}\n{i.Author}\n{i.Timestamp}\n{i.Content}\n")
    except:
        print("Could not connect to server.")
        return


if __name__ == '__main__':
    logging.basicConfig()
    while 1:
        print("\n---- Operations ----\n")
        print("1: Join a server")
        print("2: Publish an article")
        print("3: Get articles")
        print("4: Leave a server")
        print("5: Exit")
        choice = int(input())

        if choice == 1:
            ConnectToServer()

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
            LeaveServer()

        if choice == 5:
            exit(0)
