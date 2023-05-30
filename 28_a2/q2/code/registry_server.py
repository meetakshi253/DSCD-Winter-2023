from concurrent import futures
import os
import random
import logging
import shutil
import sys
import grpc
import registry_pb2
import registry_pb2_grpc
import server_pb2
import server_pb2_grpc


class Registry(registry_pb2_grpc.RegistryServicer):
    Primary = None
    Server_list = []
    Num_servers = 0

    def SetPrimary(primary_ip, primary_port):
        Registry.Primary = (primary_ip, primary_port)

    def Register(self, request, context):
        print(f"JOIN REQUEST FROM {request.ip}:{request.port}")
        try:
            if len(Registry.Server_list) >= Registry.Num_servers:
                raise Exception("Capacity reached. No more servers can be added")

            if (request.ip, request.port) in Registry.Server_list:
                raise Exception("Duplicate request")

            if not Registry.Primary:
                Registry.SetPrimary(request.ip, request.port)
            else:
                # inform the primary replica of this new replica
                InformPrimary(request.ip, request.port)
            Registry.Server_list.append((request.ip, request.port))
            return RespondAddress(Registry.Primary[0], Registry.Primary[1])

        except Exception as e:
            print(e)
            print("Could not register server. Exiting")
            exit(1)

    def GetServerList(self, request, context):
        print(f"SERVER LIST REQUEST FROM {context.peer()}")
        for server in Registry.Server_list:
            yield RespondAddress(server[0], server[1])


def RespondAddress(ip, port):
    return registry_pb2.ServerAddress(ip=ip, port=port)


def InformPrimary(replica_ip, replica_port):
    print(Registry.Primary, replica_ip, replica_port)
    primary_conn = CreateConnectionString(Registry.Primary[0], Registry.Primary[1])
    with grpc.insecure_channel(primary_conn) as channel:
        stub = server_pb2_grpc.ServerStub(channel)
        res = stub.NewJoinee(
            server_pb2.ReplicaAddress(ip=replica_ip, port=replica_port)
        )


def CreateConnectionString(ip, port):
    return f"{ip}:{port}"


def Serve():
    port = 8888
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    registry_pb2_grpc.add_RegistryServicer_to_server(Registry(), server)
    port = server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"Server started, listening on {port}")
    server.wait_for_termination()


if __name__ == "__main__":
    N = 2
    try:
        N = int(sys.argv[1])
    except:
        print(f"Invalid number of replicas, using N = {N}")

    Registry.Num_servers = N
    shutil.rmtree("../data", ignore_errors=True)
    os.mkdir("../data")
    logging.basicConfig()
    Serve()
