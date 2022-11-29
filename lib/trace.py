from .client import CLIENT
from .cache import DB
from .internal import getNormalTxns

from dataclasses import dataclass
from typing import List, Any

import time

@dataclass
class Traced:
    traces: List[Any]
    dest: str

def trace(address: str, fromblock: int, toblock: int = 20_000_000, limit = 10):
    s = time.time()
    txns = getNormalTxns(address, 0, toblock)
    if len(txns) > 100:
        return [Traced([], address)]

    if limit <= 0:
        return []

    txns = list(filter(lambda i : int(i["blockNumber"]) >= fromblock, txns))
    txns = list(filter(lambda i : i["from"] == address, txns))

    result = []
    for t in txns:
        _result = trace(t["to"], int(t["blockNumber"]), toblock, limit - 1)
        for _r in _result:
            result.append(Traced([t] + _r.traces, _r.dest))

    return result
        

