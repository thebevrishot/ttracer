from functools import lru_cache

from .client import CLIENT
from .cache import DB, R

import time

def getTxns(address: str, _from: int, _to: int):
    internal = []
    try:
        internal = CLIENT.get_internal_txs_by_address(address, _from, _to, 'asc')
    except AssertionError:
        print("assertion error")
    if len(internal) >= 10_000:
        print(f'fail on {_from} {_to}, {len(internal)}')
        mid = int((_from + _to)/2)
        x = getTxns(address, _from, mid)
        y = getTxns(address, mid, _to)
        print(type(x), type(y))
        return x + y
    else:
        print(f'success on {_from} {_to}, {len(internal)}')

    return internal

@lru_cache(maxsize=1024)
def getNormalTxns(address: str, _from: int, _to: int = 20_000_000):
    table = DB.table("addresses")
    s = time.time()
    cursor = table.get_all(address, index='address').run()

    for doc in cursor:
        # print(f'found at {time.time() - s}')
        return doc["txns"]
    # print(f'not found at {time.time() - s}')

    try:
        s = time.time()
        txns = CLIENT.get_normal_txs_by_address(address, _from, _to, 'asc')
        # print(f'queried {time.time() - s}')
    except AssertionError:
        txns = []

    s = time.time()
    table.insert([
        {
            "address": address,
            "txns": txns
        }
    ]).run()
    # print(f'inserted {time.time() - s}')

    return txns