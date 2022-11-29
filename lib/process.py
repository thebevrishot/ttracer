from typing import List
import time

def receivedByAddress(internals: List[any]):

    maps = {}
    for i in internals:
        _to = i["to"].lower()
        if _to not in maps:
            maps[_to] = 0

        maps[_to] += int(i["value"])

    return maps