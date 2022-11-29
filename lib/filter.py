def fromAddress(addr: str):
    return lambda o :  o["from"].lower() == addr.lower()