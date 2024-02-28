from web3 import Web3

from goerli_project.settings import NODE_URL

w3 = Web3(Web3.HTTPProvider(NODE_URL))
