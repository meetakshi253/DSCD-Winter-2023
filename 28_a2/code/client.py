import grpc
import uuid
import logging
from datetime import datetime

import server_pb2
import server_pb2_grpc
import registry_pb2
import registry_pb2_grpc


def GetServerList(operation):
    serverList = []
    with grpc.insecure_channel('localhost:50001') as channel:
        stub = registry_pb2_grpc.RegistryStub(channel)
        servers = stub.GetServerList(
            registry_pb2.EnquireServers(operation=operation))
        for server in servers:
            serverList.append(f"{server.ip}:{server.port}")
        return serverList


def WriteToReplicas(fileid, name, content):
    # query the write quorum
    servers = GetServerList("WRITE")
    if len(fileid) == 0:
        fileid = uuid.uuid1()  # create a new file
    # send the write request to all servers in the write quorum
    for server in servers:
        with grpc.insecure_channel(server) as channel:
            stub = server_pb2_grpc.ServerStub(channel)
            res = stub.Write(server_pb2.WriteRequest(
                uuid=fileid, name=name, content=content))
            print(res)


def DeleteFromReplicas(fileid):
    # query the write quorum
    servers = GetServerList("WRITE")
    # send the write request to all servers in the write quorum
    for server in servers:
        with grpc.insecure_channel(server) as channel:
            stub = server_pb2_grpc.ServerStub(channel)
            res = stub.Delete(server_pb2.DeleteRequest(uuid=fileid))
            print(res)


def ReadFromReplicas(fileid):
    # query the read quorum
    servers = GetServerList("READ")
    # send the read request to all servers in the read quorum
    results = []
    for server in servers:
        with grpc.insecure_channel(server) as channel:
            stub = server_pb2_grpc.ServerStub(channel)
            res = stub.Read(server_pb2.ReadRequest(uuid=fileid))
            print(res)
            if res.status.lower() == "success" or "deleted" in res.status.lower():
                results.append(res)
    latest = [results[0].version, results[0].name,
              results[0].content, results[0].status]

    for res in results[1:]:
        d1 = datetime.fromisoformat(res.version)
        d2 = datetime.fromisoformat(latest[0])
        if d1 > d2:
            latest = [res.version, res.name, res.content, res.status]

    if latest[3].lower() == "success":
        print("Latest content:\n", latest[2])
    else:
        print(latest[3])


if __name__ == '__main__':
    logging.basicConfig()

    WriteToReplicas("155", "gg1", "shdhdkdj")
    print("----")
    WriteToReplicas("155", "gg1", "new content only")
    print("----")
    ReadFromReplicas("155")
    print("----")
    # DeleteFromReplicas("kkses")
    # print("----")
    # DeleteFromReplicas("1555")
    # print("----")
    # DeleteFromReplicas("1555")
    # print("----")
    # ReadFromReplicas("1555")
