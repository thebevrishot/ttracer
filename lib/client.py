from etherscan import Etherscan
import os

API_KEY = os.getenv("ETHERSCAN_API_KEY")

# init client
CLIENT = Etherscan(API_KEY)