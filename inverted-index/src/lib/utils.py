from concurrent.futures import ThreadPoolExecutor
import grpc

from main_pb2_grpc import MainStub
from main_pb2 import RegisterRequest, WorkerReadyRequest

from lib.address import Address

from lib.config import MAIN_ADDRESS, MAX_WORKERS
from lib.statuses import SUCCESS


def register_worker(address: Address, type: str) -> None:
    try:
        with grpc.insecure_channel(str(MAIN_ADDRESS)) as channel:
            stub = MainStub(channel)
            res = stub.register(
                RegisterRequest(ip=address.ip, port=str(
                    address.port), type=type)
            )
            if not res:
                raise Exception("Could not connect to main")
            if res.status != SUCCESS:
                raise Exception("Unsuccessful join request")

            return True, res.id
    except Exception as ex:
        print(ex)

    return False, None


def worker_ready():
    try:
        with grpc.insecure_channel(str(MAIN_ADDRESS)) as channel:
            stub = MainStub(channel)
            res = stub.workerReady(WorkerReadyRequest())
            if not res:
                raise Exception("Could not connect to main")
            return True
    except Exception as ex:
        print(ex)

    return False


def serve(
    add_fn, handler, type: str, register=True, server_port="[::]:0", callback=None
) -> None:
    server = grpc.server(ThreadPoolExecutor(max_workers=MAX_WORKERS))
    add_fn(handler, server)
    address = Address(MAIN_ADDRESS.ip, server.add_insecure_port(server_port))

    server.start()

    register_status = True
    ready_status = True

    if register:
        register_status, id = register_worker(address, type)
        if register_status:
            handler.set_id(id)

    if register_status:
        print(f"'{type}' started, listening on {address.port}")
        if register:
            ready_status = worker_ready()

    if ready_status:
        if callback:
            callback()
        server.wait_for_termination(timeout=3)
    else:
        print("Terminating...")
