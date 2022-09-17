import json
from typing import Callable, Any
import os
import sys


class _Node:
    """
    The base class which defines the backend execution graph
    """

    def __init__(self, uid: str = None, funcs: dict[str, Callable] = None) -> None:
        self.uid = uid
        self.funcs = funcs
        _register_node(self)

    def evaluate(self, fn: str, *args, **kwargs):
        return self.funcs[fn](*args, **kwargs)


global_nodes: dict[str, _Node] = dict()
global_data: dict[str, Any] = dict()


def _register_node(node: _Node) -> None:
    global_nodes[node.uid] = node


def node(uid: str, **kwargs) -> None:
    _Node(uid, funcs=kwargs)


def get(x: str) -> Any:
    if x in global_data.keys():
        return global_data[x]
    else:
        return None


def set(name: str, value: Any) -> None:
    global_data[name] = value
    return value


def __process_request(calls: list) -> dict:
    response = dict()
    call_response = list()
    for call in calls:
        node = global_nodes[call['node']]
        kwargs = dict()
        for arg in call['args']:
            kwargs[arg['name']] = arg['value']
        result = node.evaluate(call['fn_name'], **kwargs)
        call_response.append(
            {'node': node.uid, 'fn_name': call['fn_name'], 'result': result})
    response['calls'] = call_response
    return response


def __get_designer(**options: dict) -> str:
    options['designer'] = {
        'persist': 'pipeline',
        'eval': 'eval'
    }
    options = json.dumps(options)
    with open('../r/inst/client.html') as f:
        html = f.read()
    html = html.replace("__options__", options)
    return html


def run_script(path: str, port: int = 8000) -> None:
    import os
    if not os.path.exists(path):
        with open(path, 'w') as f:
            pass

    servercode = """
import uvicorn
from fastapi import FastAPI
import hal9 as h9
fastapp = FastAPI()

@fastapp.post("/eval")
async def eval(calls: list):
    return h9.__process_request(calls)
uvicorn.run(fastapp, host="127.0.0.1", port=port)
"""
    with open(path, 'r') as f:
        code = f.read()
    glo = {'port': port}
    code = code + '\n' + servercode
    exec(code, glo)