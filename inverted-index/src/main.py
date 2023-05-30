import grpc
from subprocess import Popen
from uuid import uuid4
from argparse import ArgumentParser
import shutil
import os
from concurrent.futures import ThreadPoolExecutor
from math import ceil
from threading import Lock

from mapper_pb2_grpc import MapperStub
from mapper_pb2 import MapRequest, MapResponse

from reducer_pb2_grpc import ReducerStub
from reducer_pb2 import ReduceRequest, ReduceResponse

from main_pb2_grpc import MainServicer, add_MainServicer_to_server

from main_pb2 import (
    RegisterRequest,
    RegisterResponse,
    SubmissionRequest,
    SubmissionResponse,
    WorkerReadyResponse,
    WorkerReadyRequest,
)

from lib.utils import serve
from lib.address import Address

from lib.config import (
    WORKER_TYPES,
    MAIN_ADDRESS,
    WORKER_DATA,
    DATA_PATH,
    MAPPER_PATH,
    MAPPER_INPUT_PATH,
    MAPPER_OUTPUT_PATH,
    REDUCER_OUTPUT_PATH,
)
from lib.statuses import SUCCESS, FAIL


class Main(MainServicer):
    def __init__(self, n_mappers, n_reducers) -> None:
        super().__init__()
        self.lock = Lock()

        self.workers = {
            WORKER_TYPES["MAPPER"]: {},
            WORKER_TYPES["REDUCER"]: {},
        }
        self.max_workers = {
            WORKER_TYPES["MAPPER"]: n_mappers,
            WORKER_TYPES["REDUCER"]: n_reducers,
        }
        self.map_started = False
        self.reduce_started = False
        self.reducerPaths = {}
        self.outputPaths = []

        self.make_base_paths()

    def start_workers(self):
        for worker_type, n in self.max_workers.items():
            print(f"Starting {n} {worker_type}")
            for _ in range(n):
                Popen(["python3", WORKER_DATA[worker_type]["exec"]])

    def register(self, request: RegisterRequest, context):
        self.lock.acquire()
        type = request.type
        workers = self.workers[type]
        max_allowed = self.max_workers[type]
        if len(workers) >= max_allowed:
            print(
                f"Already registered {max_allowed} of type '{type}'. Rejecting worker on port = {request.port}"
            )
            return RegisterResponse(status=FAIL, id="")

        id = str(uuid4())
        workers[id] = {"address": Address(
            request.ip, request.port), "done": False}
        print(f"Registered '{type}' on port = {request.port}")
        self.lock.release()
        return RegisterResponse(status=SUCCESS, id=id)

    def make_base_paths(self):
        try:
            shutil.rmtree(DATA_PATH)
            shutil.rmtree(OUTPUT_PATH)
        except:
            pass

        os.mkdir(DATA_PATH)
        os.mkdir(OUTPUT_PATH)
        os.mkdir(MAPPER_PATH)
        os.mkdir(MAPPER_INPUT_PATH)
        os.mkdir(MAPPER_OUTPUT_PATH)
        os.mkdir(REDUCER_OUTPUT_PATH)

    def make_mapper_paths(self):
        for mapper in self.workers[WORKER_TYPES["MAPPER"]]:
            os.makedirs(os.path.join(MAPPER_INPUT_PATH, mapper))

    def make_mapper_input(self):
        inputs = os.listdir(INPUT_PATH)
        self.make_mapper_paths()
        files_per_mapper = ceil(
            len(inputs) / self.max_workers[WORKER_TYPES["MAPPER"]])
        current_mapper = 0
        mapper_keys = list(self.workers[WORKER_TYPES["MAPPER"]].keys())
        for i in range(0, len(inputs), files_per_mapper):
            for j in range(i, min(len(inputs), i + files_per_mapper)):
                shutil.copy(
                    os.path.join(INPUT_PATH, inputs[j]),
                    os.path.join(
                        MAPPER_INPUT_PATH, mapper_keys[current_mapper], inputs[j].split("Input", 1)[
                            1]
                    ),
                )
            current_mapper += 1

    def submit_map_jobs(self):
        print("Submitting map jobs...")
        try:
            for _, mapper_data in self.workers[WORKER_TYPES["MAPPER"]].items():
                with grpc.insecure_channel(str(mapper_data["address"])) as channel:
                    stub = MapperStub(channel)
                    res: MapResponse = stub.map(
                        MapRequest(
                            reducers=self.max_workers[WORKER_TYPES["REDUCER"]])
                    )
                    if not res:
                        raise Exception("Could not connect to mapper")
                    if res.status != SUCCESS:
                        raise Exception("Mapper could not map")
        except Exception as ex:
            print(ex)

    def submit_reduce_jobs(self):
        print("Submitting reduce jobs...")
        try:
            for reducer_id, reducer_data in self.workers[WORKER_TYPES["REDUCER"]].items():
                with grpc.insecure_channel(str(reducer_data["address"])) as channel:
                    stub = ReducerStub(channel)
                    filepaths = self.reducerPaths[reducer_id]
                    filemap = zip([str(i)
                                  for i in range(len(filepaths))], filepaths)
                    res: ReduceResponse = stub.reduce(
                        ReduceRequest(inputpaths=dict(filemap)))
                    if not res:
                        raise Exception("Could not connect to reducer")
                    if res.status != SUCCESS:
                        raise Exception("Reducer could not reduce")

        except Exception as ex:
            print(ex)

    def start_map(self):
        self.lock.acquire()
        self.make_mapper_input()
        self.lock.release()
        self.submit_map_jobs()

    def make_reducer_inputs(self):
        newpaths = {}
        for mapper, paths in self.reducerPaths.items():
            reducers = list(self.workers[WORKER_TYPES["REDUCER"]].keys())
            for index in range(len(paths)):
                base = os.path.dirname(paths[index])
                os.rename(paths[index],
                          f"{os.path.join(base, reducers[index])}.json",
                          )
                if not reducers[index] in newpaths:
                    newpaths[reducers[index]] = [
                        f"{os.path.join(base, reducers[index])}.json"]
                else:
                    newpaths[reducers[index]].append(
                        f"{os.path.join(base, reducers[index])}.json")
        self.reducerPaths = newpaths

    def make_final_outputs(self):
        for index, reducer_output in enumerate(self.outputPaths):
            shutil.copy(reducer_output,
                        os.path.join(OUTPUT_PATH, f"Output{index+1}.txt"))

    def start_reduce(self):
        self.lock.acquire()
        self.make_reducer_inputs()
        self.lock.release()
        self.submit_reduce_jobs()

    def workerReady(self, request: WorkerReadyRequest, context):
        resp = WorkerReadyResponse()
        if self.map_started:
            return resp

        can_start = True

        self.lock.acquire()
        for worker_type, workers in self.workers.items():
            if len(workers) != self.max_workers[worker_type]:
                can_start = False

        if can_start:
            self.map_started = True

        self.lock.release()

        if can_start:
            print("\nStarting map...")
            with ThreadPoolExecutor(max_workers=2) as executor:
                executor.submit(self.start_map)

        return resp

    def update_status(self):
        if not self.reduce_started:
            map_done = True
            for mapper in self.workers[WORKER_TYPES["MAPPER"]].values():
                if not mapper["done"]:
                    map_done = False
                    break
            if map_done:
                print("\nMap complete! Starting reduce")
                self.lock.acquire()
                self.reduce_started = True
                self.lock.release()
                with ThreadPoolExecutor(max_workers=2) as executor:
                    executor.submit(self.start_reduce)

        else:
            reduce_done = True
            for reducer in self.workers[WORKER_TYPES["REDUCER"]].values():
                if not reducer["done"]:
                    reduce_done = False
                    break
            if reduce_done:
                self.make_final_outputs()
                print("\nReduce complete! Exiting Program")

    def submitResult(self, request: SubmissionRequest, context):
        self.lock.acquire()
        self.workers[request.type][request.id]["done"] = True
        if request.type == WORKER_TYPES["MAPPER"]:
            self.reducerPaths[request.id] = list(request.reducerPaths.values())
        elif request.type == WORKER_TYPES["REDUCER"]:
            self.outputPaths.append(request.outputPath)
        self.lock.release()
        self.update_status()
        return SubmissionResponse()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "-m", "--mappers", type=int, required=True, help="Number of mappers"
    )
    parser.add_argument(
        "-r", "--reducers", type=int, required=True, help="Number of reducers"
    )

    args = parser.parse_args()
    mappers = args.mappers
    reducers = args.reducers

    global INPUT_PATH
    INPUT_PATH = input("Enter input path: ")
    global OUTPUT_PATH
    OUTPUT_PATH = input("Enter output path: ")

    main = Main(mappers, reducers)

    serve(
        add_MainServicer_to_server,
        main,
        WORKER_TYPES["MAIN"],
        False,
        f"[::]:{MAIN_ADDRESS.port}",
        lambda: main.start_workers(),
    )
