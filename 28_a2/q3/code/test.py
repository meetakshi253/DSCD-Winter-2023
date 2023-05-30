import subprocess
import time
import uuid
import client
import shutil


def start_registry():
    subprocess.Popen(['python', 'registry_server.py',
                     '4', '2', '3'])  # N, Nr, Nw


def start_servers():
    subprocess.Popen(['python', 'server.py'])
    subprocess.Popen(['python', 'server.py'])
    subprocess.Popen(['python', 'server.py'])
    subprocess.Popen(['python', 'server.py'])


def test_expected():
    subprocess.run(["kill -9 $(lsof -i :8888)"], shell=True)
    start_registry()
    time.sleep(1)
    start_servers()
    time.sleep(1)
    fileid = str(uuid.uuid1())
    filename = "file1"
    content = "some random initial content"

    try:
        cmd1 = client.WriteToReplicas(fileid, filename, content)
        assert cmd1 == True
        cmd2 = client.ReadFromReplicas(fileid)
        assert cmd2 == "some random initial content"
        cmd3 = client.DeleteFromReplicas(fileid)
        assert cmd3 == True
        cmd4 = client.ReadFromReplicas(fileid)
        assert cmd4 == "FAIL. FILE ALREADY DELETED"

    finally:
        shutil.rmtree("../data", ignore_errors=True)


def test_write():
    subprocess.run(["kill -9 $(lsof -i :8888)"], shell=True)
    start_registry()
    time.sleep(1)
    start_servers()
    time.sleep(1)
    filename = "file2"
    content = "some other random initial content"

    try:
        cmd1 = client.WriteToReplicas("", filename, content)
        assert cmd1 == True
    finally:
        shutil.rmtree("../data", ignore_errors=True)
