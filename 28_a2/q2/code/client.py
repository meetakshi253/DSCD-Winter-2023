import grpc
import uuid
import logging
from datetime import datetime

import server_pb2
import server_pb2_grpc
import registry_pb2
import registry_pb2_grpc


def GetServerList():
    serverList = []
    with grpc.insecure_channel("localhost:8888") as channel:
        stub = registry_pb2_grpc.RegistryStub(channel)
        servers = stub.GetServerList(registry_pb2.EnquireServers())
        for server in servers:
            serverList.append(f"{server.ip}:{server.port}")
        return serverList


def WriteToReplicas(fileid: str, name: str, content: str):
    # query the write quorum
    status = False
    servers = GetServerList()
    if fileid == None or len(fileid) == 0:
        fileid = str(uuid.uuid1())  # create a new file
    # send the write request to all servers in the write quorum
    for server in servers:
        with grpc.insecure_channel(server) as channel:
            stub = server_pb2_grpc.ServerStub(channel)
            res = stub.Write(
                server_pb2.WriteRequest(uuid=fileid, name=name, content=content)
            )
            print(res)
            if not "success" in res.status.lower():
                status = status or False
            else:
                status = status or True
    return status


def DeleteFromReplicas(fileid: str):
    # query the write quorum
    servers = GetServerList()
    status = False
    # send the write request to all servers in the write quorum
    for server in servers:
        with grpc.insecure_channel(server) as channel:
            stub = server_pb2_grpc.ServerStub(channel)
            res = stub.Delete(server_pb2.DeleteRequest(uuid=fileid))
            print(res)
            if not "success" in res.status.lower():
                status = status or False
            else:
                status = status or True
    return status


def ReadFromReplicas(fileid: str):
    # query the read quorum
    servers = GetServerList()
    # send the read request to all servers in the read quorum
    results = []
    for server in servers:
        with grpc.insecure_channel(server) as channel:
            stub = server_pb2_grpc.ServerStub(channel)
            res = stub.Read(server_pb2.ReadRequest(uuid=fileid))
            if res.status.lower() == "success" or "deleted" in res.status.lower():
                results.append(res)
    latest = [
        results[0].version,
        results[0].name,
        results[0].content,
        results[0].status,
    ]

    for res in results[1:]:
        d1 = datetime.fromisoformat(res.version)
        d2 = datetime.fromisoformat(latest[0])
        if d1 > d2:
            latest = [res.version, res.name, res.content, res.status]

    if latest[3].lower() == "success":
        return latest[2]
    else:
        return latest[3]


if __name__ == "__main__":
    logging.basicConfig()
    while 1:
        print("----- Enter the code corresponding to the operation -----")
        choice = int(input("1. Write to file \n2. Read from file \n3. Delete file\n"))

        if choice == 1:
            # write operation
            inp_id = input(
                "\nEnter the UUID corresponding to the file (leave empty to auto-generate uuid): "
            )
            name = input("Enter the file name: ")
            content = input("Enter the content to be written (200-500 characters): ")
            content = content[:500]  # truncated to 500 characters
            print(WriteToReplicas(inp_id, name, content))

        elif choice == 2:
            # read operation
            id = input("\nEnter the UUID corresponding to the file: ")
            print(ReadFromReplicas(id))

        elif choice == 3:
            # delete operation
            id = input("\nEnter the UUID corresponding to the file: ")
            print(DeleteFromReplicas(id))

        else:
            print("Wrong choice")

    # WriteToReplicas("1555", "gg", "shdhdkdj")
    # print("----")
    # WriteToReplicas("1555", "gg", "new content only")
    # print("----")
    # ReadFromReplicas("1555")
    # print("----")
    # DeleteFromReplicas("kkses")
    # print("----")
    # DeleteFromReplicas("1555")
    # print("----")
    # DeleteFromReplicas("1555")
    # print("----")
    # ReadFromReplicas("1555")
