# Assumption: The server does not go offline
# Bonus has been implemented

from concurrent import futures
import logging

import grpc
import time
import discord_pb2
import discord_pb2_grpc
import registry_pb2
import registry_pb2_grpc

MAXSERVERS = 12


class Registry(registry_pb2_grpc.RegistryServicer):

    servers = {}

    def Register(self, request, context):
        print(f"JOIN REQUEST FROM {request.IP}:{request.Port}")
        try:
            if len(Registry.servers) >= MAXSERVERS:
                raise Exception(
                    "Capacity reached. No more servers can be added")
            serverstring = f"{request.ServerName} - {request.IP}:{request.Port}"
            if serverstring in Registry.servers:
                raise Exception("Duplicate request")
            Registry.servers[serverstring] = True
            return registry_pb2.RegistryResponseStatus(status="SUCCESS")
        except:
            return registry_pb2.RegistryResponseStatus(status="FAIL")

    def GetServerList(self, request, context):
        print(f"SERVER LIST REQUEST FROM {context.peer()}")
        for key in Registry.servers:
            if Registry.servers[key]:
                # return live servers only
                yield registry_pb2.LiveServer(Server=key)


def HeartBeat():
    # try to connect all servers and update the status of live and dead servers
    for key in Registry.servers:
        spl = key.split(":")
        port = spl[-1]
        ip = spl[0].rsplit("-", 1)[-1].strip()
        try:
            with grpc.insecure_channel(f"{ip}:{port}") as channel:
                stub = discord_pb2_grpc.DiscordStub(channel)
                res = stub.PingPong(discord_pb2.HealthCheckRequest())
                if not res:
                    raise Exception("Server is not reachable")
        except:
            Registry.servers[key] = False  # server is not live
        finally:
            continue


def Serve():
    port = 50001
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    registry_pb2_grpc.add_RegistryServicer_to_server(Registry(), server)
    port = server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"Server started, listening on {port}")
    while 1:
        HeartBeat()
        time.sleep(5)  # check for updates every 5 seconds


if __name__ == '__main__':
    logging.basicConfig()
    Serve()
