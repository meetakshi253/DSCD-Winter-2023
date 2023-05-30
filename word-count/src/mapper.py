import os
import glob
import json
from zlib import adler32
from concurrent.futures import ThreadPoolExecutor

import grpc

from mapper_pb2_grpc import MapperServicer, add_MapperServicer_to_server
from mapper_pb2 import MapRequest, MapResponse
from main_pb2_grpc import MainStub
from main_pb2 import SubmissionRequest, SubmissionResponse

from lib.worker import Worker
from lib.utils import serve

from lib.statuses import SUCCESS
from lib.config import WORKER_TYPES, MAPPER_INPUT_PATH, MAPPER_OUTPUT_PATH, MAIN_ADDRESS


class Mapper(Worker, MapperServicer):
    def __init__(self, mapper_fn, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.mapper_fn = mapper_fn

    def set_id(self, id):
        super().set_id(id)
        self.input_path = os.path.join(MAPPER_INPUT_PATH, self.id)
        self.output_path = os.path.join(MAPPER_OUTPUT_PATH, self.id)
        os.makedirs(self.output_path)

    def partition(self, mapped_files):
        partitioned_data = []
        for i in range(self.reducers):
            partitioned_data.append([])

        for data in mapped_files:
            for key, value in data.items():
                index = adler32(bytes(key, "utf-8")) % self.reducers
                partitioned_data[index].append([key, value])

        return partitioned_data

    def save_output(self, data):
        for index in range(len(data)):
            with open(os.path.join(self.output_path, f"i-{index}.json"), "w") as file:
                json.dump(data[index], file)
            file.close()

    def map_complete(self):
        try:
            with grpc.insecure_channel(str(MAIN_ADDRESS)) as channel:
                stub = MainStub(channel)
                filepaths = glob.glob(os.path.join(self.output_path, '*'))
                filemap = zip([str(i)
                              for i in range(len(filepaths))], filepaths)
                res: SubmissionResponse = stub.submitResult(
                    SubmissionRequest(
                        type=WORKER_TYPES["MAPPER"], status=SUCCESS, id=self.id, reducerPaths=dict(
                            filemap)
                    )
                )
                if not res:
                    raise Exception("Could not connect to main")
        except Exception as ex:
            print(ex)

    def start_map(self):
        inputs = os.listdir(self.input_path)
        mapped_files = []
        for input in inputs:
            with open(os.path.join(self.input_path, input), "r") as file:
                mapped_files.append(self.mapper_fn(file.read()))
            file.close()

        partitioned_data = self.partition(mapped_files)
        self.save_output(partitioned_data)
        self.map_complete()

    def map(self, request: MapRequest, context):
        self.reducers = request.reducers
        with ThreadPoolExecutor(max_workers=2) as executor:
            executor.submit(self.start_map)
        executor.shutdown(wait=True)
        return MapResponse(status=SUCCESS)


if __name__ == "__main__":

    def mapper_fn(text):
        res = {}
        for word in text.split():
            word = word.lower()
            if word in res:
                res[word] += 1
            else:
                res[word] = 1

        return res

    serve(add_MapperServicer_to_server, Mapper(
        mapper_fn), WORKER_TYPES["MAPPER"])
