import pika
import uuid
import json

CLIENTNAME = str(uuid.uuid1())
JOINEDSERVERS = []


class DiscordClient(object):

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

    def GetServerList(self):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        message = StringifyMessage(
            {"method": "GetServerList", "args": {"id": CLIENTNAME}})
        self.channel.basic_publish(exchange='', routing_key='registry', properties=pika.BasicProperties(
            reply_to=self.callback_queue,
            correlation_id=self.corr_id,
        ), body=message)
        self.connection.process_data_events(time_limit=1)
        res = ParseJson(self.response)
        return res["servers"]

    def ConnectToServer(self):
        global JOINEDSERVERS
        serverList = discord.GetServerList()
        print("List of servers:")
        for servername in serverList:
            print(servername)
        choice = input("\nEnter the name of the server you wish to join: ")
        print("Attempting to contact the server", choice)
        try:
            self.response = None
            self.corr_id = str(uuid.uuid4())
            message = StringifyMessage(
                {"args": {"id": CLIENTNAME}, "method": "JoinServer"})
            self.channel.basic_publish(exchange='', routing_key=choice, properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ), body=message)
            self.connection.process_data_events(time_limit=1)
            res = ParseJson(self.response)
            print(res["status"])
            if (res["status"].lower() == "success"):
                JOINEDSERVERS.append(choice)
        except:
            print("Could not connect to server.\nFAIL")
            return

    def LeaveServer(self):
        if len(JOINEDSERVERS) == 0:
            print("Join a server first\nFAIL")
            return
        choice = input(f"Which server do you want to leave? {JOINEDSERVERS} ")
        try:
            self.response = None
            self.corr_id = str(uuid.uuid4())
            message = StringifyMessage(
                {"args": {"id": CLIENTNAME}, "method": "LeaveServer"})
            self.channel.basic_publish(exchange='', routing_key=choice, properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ), body=message)
            self.connection.process_data_events(time_limit=1)
            res = ParseJson(self.response)
            print(res["status"])
            if res["status"].lower() == "success":
                JOINEDSERVERS.remove(choice)
        except:
            print("Could not connect to server.\nFAIL")
            return

    def PushArticle(self, atype, author, content):
        if len(JOINEDSERVERS) == 0:
            print("Join a server first\nFAIL")
            return
        if not atype.lower() in ["sports", "fashion", "politics"] or len(author) == 0 or len(content) == 0:
            print("FAIL")
            return
        self.corr_id = str(uuid.uuid4())
        self.response = None
        choice = input(
            f"Which server do you want to publish to? {JOINEDSERVERS} ")
        article = {"type": atype, "author": author, "content": content[:200]}
        message = StringifyMessage({"method": "PublishArticle", "args": {
            "id": CLIENTNAME, "article": article}})
        self.channel.basic_publish(exchange='', routing_key=choice, properties=pika.BasicProperties(
            reply_to=self.callback_queue,
            correlation_id=self.corr_id,
        ), body=message)
        self.connection.process_data_events(time_limit=1)
        res = ParseJson(self.response)
        print(res["status"])

    def RequestArticles(self, atype, author, date):
        if len(JOINEDSERVERS) == 0:
            print("Join a server first\nFAIL")
            return
        self.corr_id = str(uuid.uuid4())
        self.response = None
        choice = input(
            f"Which server do you want to get articles from? {JOINEDSERVERS} ")
        articleTags = {"type": atype, "author": author, "timestamp": date}
        message = StringifyMessage({"method": "GetArticles", "args": {
            "id": CLIENTNAME, "article": articleTags}})
        self.channel.basic_publish(exchange='', routing_key=choice, properties=pika.BasicProperties(
            reply_to=self.callback_queue,
            correlation_id=self.corr_id,
        ), body=message)
        self.connection.process_data_events(time_limit=1)
        res = ParseJson(self.response)
        print(res["status"])
        if (res["status"] == "FAIL"):
            return
        articles = res["articles"]
        count = 0
        for article in articles:
            count += 1
            print(f"{count})")
            print(
                f"{article['type'].upper()}\n{article['author']}\n{article['timestamp']}\n{article['content']}\n")


def StringifyMessage(message):
    return json.dumps(message)


def ParseJson(message):
    return json.loads(message)


if __name__ == '__main__':
    discord = DiscordClient()
    while 1:
        print("\n---- Operations ----\n")
        print("1: Join a server")
        print("2: Publish an article")
        print("3: Get articles")
        print("4: Leave a server")
        print("5: Exit")
        choice = int(input())

        if choice == 1:
            discord.ConnectToServer()

        if choice == 2:
            atype = input(
                "Enter the article type (sports/fashion/politics): ")
            author = input("Enter the author name: ")
            content = input(
                "Enter the article content (only 200 characters, rest would be truncated): ")
            discord.PushArticle(atype, author, content)

        if choice == 3:
            print("Enter the tags. Leave a blank if you do not wish to specify.")
            atype = input(
                "Enter the article type (sports/fashion/politics): ")
            author = input("Enter the author name: ")
            date = input("Enter date of publishing (dd/mm/yyyy): ")
            discord.RequestArticles(atype, author, date)

        if choice == 4:
            discord.LeaveServer()

        if choice == 5:
            exit(0)
