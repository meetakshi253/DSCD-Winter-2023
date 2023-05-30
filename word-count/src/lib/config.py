from lib.address import Address
import os

IP = "localhost"
MAIN_ADDRESS = Address(IP, 8888)

MAX_WORKERS = 8

WORKER_TYPES = {
    "MAPPER": "MAPPER",
    "REDUCER": "REDUCER",
    "MAIN": "MAIN",
}


WORKER_DATA = {
    WORKER_TYPES["MAPPER"]: {"exec": "./mapper.py"},
    WORKER_TYPES["REDUCER"]: {"exec": "./reducer.py"},
}

INPUT_PATH = os.path.join("..", "input")

DATA_PATH = os.path.join("..", "data")
REDUCER_OUTPUT_PATH = os.path.join(DATA_PATH, "output")

MAPPER_PATH = os.path.join(DATA_PATH, "mapper")
MAPPER_INPUT_PATH = os.path.join(MAPPER_PATH, "input")
MAPPER_OUTPUT_PATH = os.path.join(MAPPER_PATH, "output")
