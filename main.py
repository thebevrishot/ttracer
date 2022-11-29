from lib.internal import getTxns
import lib.internal as libinternal
import lib.sort as libsort
import lib.filter as libfilter
import lib.process as libprocess
import lib.trace as libtrace
import json

import sys

from os import path


CONTRACT = "0xA160cdAB225685dA1d56aa342Ad8841c3b53f291"

# load
FILE = "ETH_INTERNAL_TXNS.json"
FROM = 15323740

internals = []
if path.exists(FILE):
     with open("ETH_INTERNAL_TXNS.json", "r") as r:
        internals = json.load( r )
else:
    internals = getTxns(CONTRACT, 0, 20_000_000)
    print(len(internals))

    with open("ETH_INTERNAL_TXNS.json", "w") as w:
        json.dump( internals, w )


def print_ts():
    for i in internals[:100]:
        print(i["timeStamp"])

libsort.internal(internals, 'desc')

filtered = list(filter(libfilter.fromAddress(CONTRACT), internals))

def after(i):
    t = int(i["timeStamp"])
    return t > 1660262399 and t < 1662940799
filtered = list(filter(after, filtered))

receivedMap = libprocess.receivedByAddress(filtered)
receiveds = list(receivedMap.items())
receiveds.sort(key = lambda r : r[1], reverse=True)

# ordering
# print(len(receivedMap))
# for r in receiveds[:100]:
#     print(r)

# txns = libinternal.getNormalTxns("0x377ae2e4987dfbb9585fd8967efbe9823d281b1c", 0)
# print(txns)

# tranced = libtrace.trace("0x6c2bf6d9f29cee3ea7641f593cdd3e855ee5d288", 15323740)

# print(tranced)

tranceds = []
ct = 0
for rec in receiveds:
    sys.stdout.write('\r')
    (address, amount) = rec
    _tranceds = libtrace.trace(address, 15323740)
    tranceds += _tranceds
    ct += 1
    sys.stdout.write(f'progress {ct}/{len(receiveds)} {libinternal.getNormalTxns.cache_info()}')
    sys.stdout.flush()

# max count
from dataclasses import dataclass

class DestResult:
    address: str
    count: int = 0
    all_value: int = 0

results = {}

for t in tranceds:
    if t.dest not in results:
        results[t.dest] = {
            "dest": t.dest,
            "count": 0,
            "all_value": 0 
        }
    results[t.dest]["count"] += 1
    
    if len(t.traces) > 0:
        last_txn = t.traces[len(t.traces) - 1]
        results[t.dest]["all_value"] += int(last_txn['value'])

from lib.cache import DB
print(len(results))
for (a, value) in results.items():
    DB.table("dest").insert(value).run()