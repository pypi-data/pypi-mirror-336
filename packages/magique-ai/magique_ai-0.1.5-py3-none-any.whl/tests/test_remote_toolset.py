import sys

from magique.client import MagiqueError
from magique.ai.toolset import tool, ToolSet, run_toolsets
from magique.ai.utils.remote import connect_remote
from magique.ai.tools.web_browse import WebBrowseToolSet
from magique.ai.tools.python.python_interpreter import PythonInterpreterToolSet, PythonInterpreterError
from magique.ai.tools.r.r_interpreter import RInterpreterToolSet
from magique.ai.tools.shell import ShellToolSet
from executor.engine import Engine, LocalJob, ProcessJob

import pytest


def test_remote_toolset():

    class MyToolSet(ToolSet):
        @tool(job_type="thread")
        def my_tool(self):
            return "Hello, world!"

    my_toolset = MyToolSet("my_toolset")
    assert len(my_toolset.worker.functions) == 1
    

async def test_web_browse_toolset():
    toolset = WebBrowseToolSet("web_browse")

    async def start_toolset():
        await toolset.run()

    with Engine() as engine:
        job = ProcessJob(start_toolset)
        engine.submit(job)
        await job.wait_until_status("running")
        s = await connect_remote(toolset.service_id)
        try:
            res = await s.invoke("duckduckgo_search", {"query": "Hello, world!"})
            assert len(res) > 0
            await job.cancel()
            await engine.wait_async()
        except MagiqueError as e:
            print(e)


async def test_python_interpreter_toolset():
    toolset = PythonInterpreterToolSet("python_interpreter")

    async def start_toolset():
        await toolset.run()

    with Engine() as engine:
        job = ProcessJob(start_toolset)
        await engine.submit_async(job)
        await job.wait_until_status("running")
        s = await connect_remote(toolset.service_id)
        with pytest.raises(MagiqueError):
            resp = await s.invoke("run_code", {"code": "xxxxx"})
        resp = await s.invoke("run_code", {"code": "res = 1 + 1", "result_var_name": "res"})
        assert resp["result"] == 2
        resp = await s.invoke("run_code", {"code": "", "result_var_name": "res"})
        assert resp["result"] == 2
        await job.cancel()
        await engine.wait_async()


async def test_r_toolset():
    toolset = RInterpreterToolSet("r_interpreter")

    async with run_toolsets([toolset]):
        s = await connect_remote(toolset.service_id)
        await s.invoke("run_code", {"code": "a <- 1 + 1"})
        resp = await s.invoke("run_code", {"code": "a"})
        assert resp.strip() == "[1] 2"


async def test_shell_toolset():
    toolset = ShellToolSet("shell")

    async with run_toolsets([toolset]):
        s = await connect_remote(toolset.service_id)
        if sys.platform.startswith("win"):
            command = "dir"
        else:
            command = "ls"
        await s.invoke("run_command", {"command": command})
        resp = await s.invoke("run_command", {"command": "echo 'Hello, world!'"})
        assert "Hello, world!" in resp
