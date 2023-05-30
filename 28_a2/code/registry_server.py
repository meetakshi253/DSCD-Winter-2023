from concurrent import futures
import os
import random
import logging
import shutil

import grpc
import registry_pb2
import registry_pb2_grpc
import server_pb2
import server_pb2_grpc


class Registry(registry_pb2_grpc.RegistryServicer):

    Primary = None
    Server_list = []
    Num_servers = 0
    Read_quorum = 0
    Write_quorum = 0

    def SetPrimary(primary_ip, primary_port):
        Registry.Primary = (primary_ip, primary_port)

    def Register(self, request, context):
        print(f"JOIN REQUEST FROM {request.ip}:{request.port}")
        try:
            if len(Registry.Server_list) >= Registry.Num_servers:
                raise Exception(
                    "Capacity reached. No more servers can be added")

            if (request.ip, request.port) in Registry.Server_list:
                raise Exception("Duplicate request")

            if not Registry.Primary:
                Registry.SetPrimary(request.ip, request.port)
            else:
                # inform the primary replica of this new replica
                InformPrimary(request.ip, request.port)
            Registry.Server_list.append((request.ip, request.port))
            return RespondAddress(Registry.Primary[0], Registry.Primary[1])

        except:
            print("Could not register server. Exiting")
            exit(1)

    def GetServerList(self, request, context):
        print(f"SERVER LIST REQUEST FROM {context.peer()}")
        n = Quorum(request.operation)
        if n == 0:
            print("Invalid request")
        for entry in random.sample(Registry.Server_list, n):
            yield RespondAddress(entry[0], entry[1])


def RespondAddress(ip, port):
    return registry_pb2.ServerAddress(ip=ip, port=port)


def InformPrimary(replica_ip, replica_port):
    print(Registry.Primary, replica_ip, replica_port)
    primary_conn = CreateConnectionString(
        Registry.Primary[0], Registry.Primary[1])
    with grpc.insecure_channel(primary_conn) as channel:
        stub = server_pb2_grpc.ServerStub(channel)
        res = stub.NewJoinee(server_pb2.ReplicaAddress(
            ip="localhost", port='202'))
    # try:
    #     with grpc.insecure_channel(primary_conn) as channel:
    #         stub = server_pb2_grpc.ServerStub(channel)
    #         res = stub.NewJoinee(server_pb2.ServerAddress(
    #             ip=replica_ip, port=replica_port))
    #         if not res:
    #             raise Exception
    # except:
    #     print("Replica not reachable.")
    #     exit(1)


def Quorum(operation):
    if operation.lower() == "read":
        return Registry.Read_quorum
    elif operation.lower() == "write":
        return Registry.Write_quorum
    else:
        return 0


def CreateConnectionString(ip, port):
    return f"{ip}:{port}"


def ValidateQuorum(N, Nr, Nw):
    result = False
    if Nw > N/2:
        result = not result
    else:
        print("Number of replicas in the write quorum should be greater than N/2.")
    if Nw+Nr > N:
        pass
    else:
        result = not result
        print("Number of replicas in the read quorum should be greater than N-Nw.")
    return result


def Serve():
    port = 50001
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    registry_pb2_grpc.add_RegistryServicer_to_server(Registry(), server)
    port = server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"Server started, listening on {port}")
    server.wait_for_termination()


if __name__ == '__main__':
    valid = False
    while (not valid):
        N = int(input("Enter the number of replicas (N): "))
        Nr = int(input("Enter the read quorum: "))
        Nw = int(input("Enter the write quorum: "))
        valid = ValidateQuorum(N, Nr, Nw)

    Registry.Num_servers = N
    Registry.Read_quorum = Nr
    Registry.Write_quorum = Nw
    shutil.rmtree("../data", ignore_errors=True)
    os.mkdir("../data")
    logging.basicConfig()
    Serve()
