import logging
import random
import string
import time
from http import HTTPStatus

from rest_framework.response import Response
from web3.exceptions import TransactionNotFound

from api.connector import w3
from goerli_project.settings import ABI, CONTRACT, PRIVAT_KEY
from logging_config import configure_logging
from tokens.models import Token

CHAIN_ID = 5
GAS = 2_000_000

configure_logging()


def generate_token_id(length=20):
    characters = string.ascii_letters + string.digits
    unique_hash = ''.join(random.choice(characters) for _ in range(length))
    if Token.objects.filter(unique_hash=unique_hash).exists():
        raise ValueError('Token с таким unique_hash уже существует')
    return unique_hash


def create_txn(owner, token_id, media_url):
    unicorns = w3.eth.contract(address=CONTRACT, abi=ABI)
    return unicorns.functions.mint(
        owner,
        token_id,
        media_url
    ).build_transaction({
        'chainId': CHAIN_ID,
        'gas': GAS,
        'maxFeePerGas': w3.to_wei('2', 'gwei'),
        'maxPriorityFeePerGas': w3.to_wei('1', 'gwei'),
        'nonce': w3.eth.get_transaction_count(owner),
    })


def get_supply(address=CONTRACT, abi=ABI):
    unicorns = w3.eth.contract(address=address, abi=abi)
    return unicorns.functions.totalSupply().call()


def check_txn_status(txn, status=None):
    while not status:
        try:
            status = str(w3.eth.get_transaction_receipt(
                txn.hex()
            )['status'])
            break
        except TransactionNotFound:
            status = None
            time.sleep(10)


def send_txn(unicorn_txn):
    try:
        signed_txn = w3.eth.account.sign_transaction(
            unicorn_txn,
            private_key=PRIVAT_KEY
        )
        txn = w3.eth.send_raw_transaction(
            signed_txn.rawTransaction
        )
        check_txn_status(txn)
    except ValueError as e:
        logging.error(f'{e}')
        return Response(
            {'message': f'Возникли проблемы с отправкой транзакции: {e}'},
            status=HTTPStatus.BAD_REQUEST
        )
    return txn
