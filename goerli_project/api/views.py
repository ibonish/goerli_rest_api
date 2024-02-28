from http import HTTPStatus

from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.connector import w3
from api.serializers import TokenCreateSerializer, TokenSerializer
from api.utils import generate_token_id
from goerli_project.settings import ABI, CONTRACT, PRIVAT_KEY
from tokens.models import Token

CHAIN_ID = 5
GAS = 2_000_000


@api_view(['POST'])
def create_token(request):
    """
    Создание токена.
    Эндпоинт:
      * - tokens/create/
    Request body:
      {
        "media_url": "<урл с произвольным изображением>",
        "owner": "<адресс владельца токена>",
      }
    """
    owner = request.data['owner']
    media_url = request.data['media_url']
    token_id = generate_token_id()
    unicorns = w3.eth.contract(address=CONTRACT, abi=ABI)
    unicorn_txn = unicorns.functions.mint(
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
    try:
        signed_txn = w3.eth.account.sign_transaction(
            unicorn_txn,
            private_key=PRIVAT_KEY
        )
        txn = w3.eth.send_raw_transaction(
            signed_txn.rawTransaction
        )
    except ValueError as e:
        # TODO: логирование
        Response(
            {'message': f'Возникли проблемы с отправкой транзакции {e}'},
            status=HTTPStatus.BAD_REQUEST
        )
    serializer = TokenCreateSerializer(
        data={
            'unique_hash': token_id,
            'tx_hash': txn.hex(),
            'media_url': media_url,
            'owner': owner
        }
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=HTTPStatus.CREATED)
    return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)


@api_view(['GET'])
def get_token_list(request):
    """
    Просмотр всех созданных токенов.
    Эндпоинт:
      * - tokens/list/
    """
    tokens = Token.objects.all()
    serializer = TokenSerializer(tokens, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_total_supply(request):
    """
    Информация о текущем Total supply токена.
    Эндпоинт:
      * - tokens/total_supply/
    """
    unicorns = w3.eth.contract(address=CONTRACT, abi=ABI)
    total_supply = unicorns.functions.totalSupply().call()
    return Response({'result': f'{total_supply}'})
