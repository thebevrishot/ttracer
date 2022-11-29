from typing import List

def internal(internals:  List[any], _sort: str):
    keyFunc = lambda i : int(i["timeStamp"])
    internals.sort(key=keyFunc, reverse=_sort == "desc")
    return internals