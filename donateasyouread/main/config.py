import os

from dotenv import load_dotenv
from web3 import Web3


load_dotenv()

web3 = Web3(Web3.HTTPProvider(os.environ.get('INFURA_URL')))
