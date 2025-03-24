import os
from magique.ai.tools.file_manager.client import FileManagerClient
from magique.ai.tools.file_manager.worker import FileManagerToolSet
from magique.ai.toolset import run_toolsets
from tempfile import TemporaryDirectory


async def test_file_manager():
    test_file = "test.txt"
    with open(test_file, "w") as f:
        f.write("Hello, world!" * 1000)

    test_output_file = "test_output.txt"
    with TemporaryDirectory() as temp_dir:
        toolset = FileManagerToolSet("file_manager", temp_dir)
        async with run_toolsets([toolset]):
            client = FileManagerClient("file_manager", connect_params={"try_direct_connection": False})
            await client.send_file(test_file, "test.txt", chunk_size=10000)
            await client.fetch_file(test_output_file, "test.txt", chunk_size=10000)
            with open(test_output_file, "r") as f:
                assert f.read() == "Hello, world!" * 1000

    os.remove(test_file)
    os.remove(test_output_file)
