import os
from concurrent.futures import ThreadPoolExecutor
import json

import grpc

from reducer_pb2_grpc import ReducerServicer, add_ReducerServicer_to_server
from reducer_pb2 import ReduceRequest, ReduceResponse
from main_pb2_grpc import MainStub
from main_pb2 import SubmissionRequest, SubmissionResponse

from lib.worker import Worker
from lib.utils import serve

from lib.statuses import SUCCESS
from lib.config import WORKER_TYPES, MAPPER_OUTPUT_PATH, REDUCER_OUTPUT_PATH, MAIN_ADDRESS


class Reducer(Worker, ReducerServicer):
    def __init__(self, reducer_fn, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.reducer_fn = reducer_fn
        self.input_paths = []

    def set_id(self, id):
        super().set_id(id)
        self.input_path = os.path.join(MAPPER_OUTPUT_PATH, self.id)
        self.output_path = os.path.join(REDUCER_OUTPUT_PATH, f"{self.id}.txt")

    def shuffle(self):
        inputdata = []
        for input in self.input_paths:
            with open(input, "r") as file:
                inputdata.extend(json.load(file))
            file.close()
        return inputdata

    def sort(self, raw_input):
        res = {}
        for input in raw_input:
            word, id = input
            if word in res:
                res[word].append(id)
            else:
                res[word] = list([id])
        return res

    def save_output(self, data):
        with open(self.output_path, "w") as file:
            for word, ids in data:
                file.write(f"{word} {', '.join(ids)}\n")
        file.close()

    def reduce_complete(self):
        try:
            with grpc.insecure_channel(str(MAIN_ADDRESS)) as channel:
                stub = MainStub(channel)
                res: SubmissionResponse = stub.submitResult(
                    SubmissionRequest(
                        type=WORKER_TYPES["REDUCER"], status=SUCCESS, id=self.id, outputPath=self.output_path
                    )
                )
                if not res:
                    raise Exception("Could not connect to main")
        except Exception as ex:
            print(ex)

    def start_reduce(self):
        raw_input = self.shuffle()
        sorted_inputs = self.sort(raw_input)
        reduced_outputs = []
        for key, value in sorted_inputs.items():
            reduced_outputs.append(self.reducer_fn(key, value))

        self.save_output(reduced_outputs)
        self.reduce_complete()

    def reduce(self, request: ReduceRequest, context):
        self.input_paths = list(request.inputpaths.values())
        with ThreadPoolExecutor(max_workers=2) as executor:
            executor.submit(self.start_reduce)
        executor.shutdown(wait=True)
        return ReduceResponse(status=SUCCESS)


if __name__ == "__main__":

    def reducer_fn(word: str, ids: list[int]):
        return ((word, list(set(ids))))

    serve(add_ReducerServicer_to_server, Reducer(
        reducer_fn), WORKER_TYPES["REDUCER"])
