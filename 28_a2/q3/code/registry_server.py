from concurrent import futures
import os
import math
import random
import logging
import shutil
import sys

import grpc
import registry_pb2
import registry_pb2_grpc


class Registry(registry_pb2_grpc.RegistryServicer):

    Server_list = []
    Num_servers = 0

    def Register(self, request, context):
        print(f"JOIN REQUEST FROM {request.ip}:{request.port}")
        try:
            if len(Registry.Server_list) >= Registry.Num_servers:
                raise Exception(
                    "Capacity reached. No more servers can be added")

            if (request.ip, request.port) in Registry.Server_list:
                raise Exception("Duplicate register request")

            Registry.Server_list.append((request.ip, request.port))
            print(Registry.Server_list)
            return registry_pb2.Response(status="SUCCESS")

        except:
            print("Could not register server")
            return registry_pb2.Response(status="FAIL")

    def GetServerList(self, request, context):
        print(f"SERVER LIST REQUEST FROM {context.peer()}")
        n = Quorum(request.operation)
        print(n, Registry.Server_list)
        try:
            for entry in random.sample(Registry.Server_list, n):
                print(entry, type(entry))
                yield registry_pb2.ServerAddress(ip=entry[0], port=entry[1])
        except:
            yield registry_pb2.ServerAddress(ip="1", port="2")
        # if n == 0:
        #     print("Invalid request")
        #     yield registry_pb2.ServerAddress(None, None)
        # print("here", random.sample(Registry.Server_list, n))


def Quorum(operation):  # try putting wrong operation
    if operation.lower() == "read":
        return Registry.Read_quorum
    elif operation.lower() == "write":
        return Registry.Write_quorum
    else:
        return 0


def ValidateQuorum(N, Nr, Nw):
    if not (Nw > math.floor(N/2)):
        print(
            f"Number of replicas in the write quorum should be greater than {math.floor(N/2)}.")
        return False
    if not (Nw+Nr > N):
        print(
            f"Number of replicas in the read quorum should be greater than {N-Nw}.")
        return False
    return True


def Serve():
    port = 8888
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    registry_pb2_grpc.add_RegistryServicer_to_server(Registry(), server)
    port = server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"Server started, listening on port {port}")
    server.wait_for_termination()


if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) != 3:
        print("Wrong params. Exiting")
        exit(1)
    N = int(args[0])
    Nr = int(args[1])
    Nw = int(args[2])

    valid = False
    valid = ValidateQuorum(N, Nr, Nw)
    if not valid:
        exit(1)

    # while (not valid):
    #     N = int(input("Enter the number of replicas (N): "))
    #     Nr = int(input("Enter the read quorum: "))
    #     Nw = int(input("Enter the write quorum: "))
    #     valid = ValidateQuorum(N, Nr, Nw)
    #     print(valid)

    Registry.Num_servers = N
    Registry.Read_quorum = Nr
    Registry.Write_quorum = Nw
    shutil.rmtree("../data", ignore_errors=True)
    os.mkdir("../data")
    logging.basicConfig()
    Serve()
