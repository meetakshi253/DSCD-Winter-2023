from concurrent import futures
from datetime import datetime
import logging
import uuid
import os

import grpc
import server_pb2
import server_pb2_grpc
import registry_pb2
import registry_pb2_grpc

IP = "localhost"
PORT = None


class Server(server_pb2_grpc.ServerServicer):
    Max_clients = 10
    Server_directory = f"../data/{uuid.uuid4()}/"
    Memstore = {}  # the in-memory key-value store
    Primary = None
    Backup_replicas = []

    def SetPrimary(primary_ip, primary_port):
        Server.Primary = (primary_ip, primary_port)

    def NewJoinee(self, request, context):
        if IP == Server.Primary[0] and PORT == Server.Primary[1]:
            Server.Backup_replicas.append((request.ip, request.port))
        return server_pb2.JoinResponse(status="SUCCESS")

    def Read(self, request: server_pb2.ReadRequest, context):
        print(Server.Memstore)
        childfiles = os.listdir(Server.Server_directory)

        if request.uuid not in Server.Memstore.keys():
            # client is trying to read a file that does not exist
            return server_pb2.ReadResponse(status="FAIL. FILE DOES NOT EXIST")
        elif (
            request.uuid in Server.Memstore.keys()
            and Server.Memstore[request.uuid][0] in childfiles
        ):
            # client is trying to read an exisiting file
            file = open(
                f"{Server.Server_directory}/{Server.Memstore[request.uuid][0]}", "r"
            )
            content = file.read()
            return server_pb2.ReadResponse(
                status="SUCCESS",
                content=content,
                name=Server.Memstore[request.uuid][0],
                version=Server.Memstore[request.uuid][1],
            )
        elif (
            request.uuid in Server.Memstore.keys()
            and Server.Memstore[request.uuid][0] not in childfiles
        ):
            # client is trying to read a deleted file
            return server_pb2.ReadResponse(
                status="FAIL. FILE ALREADY DELETED",
                version=Server.Memstore[request.uuid][1],
                content=None,
            )

    def Write(self, request: server_pb2.WriteRequest, context):
        timestamp = datetime.isoformat(datetime.now())
        if not request.uuid:
            request.uuid = uuid.uuid4()

        if IP == Server.Primary[0] and PORT == Server.Primary[1]:
            for server in self.Backup_replicas:
                server = ":".join(server)
                with grpc.insecure_channel(server) as channel:
                    stub = server_pb2_grpc.ServerStub(channel)
                    res = stub.PrimaryWrite(
                        server_pb2.PrimaryWriteRequest(
                            name=request.name,
                            content=request.content,
                            uuid=request.uuid,
                            version=timestamp,
                        )
                    )
                    if not res or res.status.lower() != "success":
                        if not res:
                            return server_pb2.WriteResponse(
                                status="FAIL. BACKUP FAILED TO WRITE"
                            )
                        return res

            self.DoWrite(request.uuid, request.name, timestamp, request.content)

            return server_pb2.WriteResponse(
                status="SUCCESS", uuid=request.uuid, version=timestamp
            )

        else:
            with grpc.insecure_channel(":".join(Server.Primary)) as channel:
                stub = server_pb2_grpc.ServerStub(channel)
                res = stub.Write(request)
                if not res:
                    server_pb2.WriteResponse(status="FAIL. PRIMARY FAILED TO WRITE.")
                return res

    def Delete(self, request: server_pb2.DeleteRequest, context):
        timestamp = datetime.isoformat(datetime.now())

        if IP == Server.Primary[0] and PORT == Server.Primary[1]:
            for server in self.Backup_replicas:
                server = ":".join(server)
                with grpc.insecure_channel(server) as channel:
                    stub = server_pb2_grpc.ServerStub(channel)
                    res = stub.PrimaryDelete(
                        server_pb2.PrimaryDeleteRequest(
                            uuid=request.uuid, version=timestamp
                        )
                    )

                    if not res or res.status.lower() != "success":
                        if not res:
                            return server_pb2.DeleteResponse(
                                status="FAIL. PRIMARY FAILED TO DELETE"
                            )
                        return res

            self.DoDelete(request.uuid, timestamp)
            return server_pb2.DeleteResponse(status="SUCCESS")

        else:
            with grpc.insecure_channel(":".join(Server.Primary)) as channel:
                stub = server_pb2_grpc.ServerStub(channel)
                res = stub.Delete(request)
                if not res:
                    server_pb2.WriteResponse(status="FAIL. PRIMARY FAILED TO WRITE.")
                return res

    def DoWrite(self, uuid, name, timestamp, content):
        Server.Memstore[uuid] = (name, timestamp)
        with open(f"{Server.Server_directory}/{name}", "w") as file:
            file.write(content)

    def DoDelete(self, uuid, timestamp):
        os.remove(f"{Server.Server_directory}/{Server.Memstore[uuid][0]}")
        Server.Memstore[uuid] = ("", timestamp)

    def PrimaryWrite(self, request: server_pb2.PrimaryWriteRequest, context):
        childfiles = os.listdir(Server.Server_directory)
        timestamp = request.version

        if (
            request.uuid not in Server.Memstore.keys()
            and request.name not in childfiles
        ):
            self.DoWrite(request.uuid, request.name, timestamp, request.content)
        elif request.uuid not in Server.Memstore.keys() and request.name in childfiles:
            # client is trying to create another file with the same nam
            return server_pb2.WriteResponse(
                status="FAIL. FILE WITH THE SAME NAME ALREADY EXISTS"
            )
        elif request.uuid in Server.Memstore.keys() and request.name in childfiles:
            # client is trying to update an exisiting file
            self.DoWrite(request.uuid, request.name, timestamp, request.content)
        else:
            # client is trying to update a deleted file
            return server_pb2.WriteResponse(
                status="FAIL. DELETED FILE CANNOT BE UPDATED"
            )

        return server_pb2.WriteResponse(
            status="SUCCESS", uuid=request.uuid, version=timestamp
        )

    def PrimaryDelete(self, request: server_pb2.PrimaryDeleteRequest, context):
        childfiles = os.listdir(Server.Server_directory)
        if request.uuid not in Server.Memstore.keys():
            # client is trying to read a file that does not exist
            Server.Memstore[request.uuid] = ("", request.version)
            return server_pb2.DeleteResponse(
                status="FILE DOES NOT EXIST ON THIS REPLICA"
            )
        elif (
            request.uuid in Server.Memstore.keys()
            and Server.Memstore[request.uuid][0] in childfiles
        ):
            self.DoDelete(request.uuid, request.version)
        elif (
            request.uuid in Server.Memstore.keys()
            and Server.Memstore[request.uuid][0] not in childfiles
        ):
            return server_pb2.DeleteResponse(status="FAIL. FILE ALREADY DELETED.")

        return server_pb2.DeleteResponse(status="SUCCESS")


def RegisterServer():
    print("Attempting to register the server...")
    try:
        with grpc.insecure_channel("localhost:8888") as channel:
            stub = registry_pb2_grpc.RegistryStub(channel)
            res = stub.Register(registry_pb2.ServerAddress(ip=IP, port=PORT))
            print(res)
            if not res:
                print("here")
                raise Exception
            Server.Primary = (res.ip, res.port)
    except:
        print("Could not register the server")  # fix this


def serve():
    global PORT
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server_pb2_grpc.add_ServerServicer_to_server(Server(), server)
    port = server.add_insecure_port("[::]:0")
    PORT = str(port)
    server.start()
    RegisterServer()
    print(f"Server started, listening on {port}")
    server.wait_for_termination()


if __name__ == "__main__":
    os.mkdir(Server.Server_directory)
    logging.basicConfig()
    serve()
