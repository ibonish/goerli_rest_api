import logging
from http import HTTPStatus

from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.paginations import CustomPagination
from api.serializers import TokenCreateSerializer, TokenSerializer
from api.utils import create_txn, generate_token_id, get_supply, send_txn
from api.validators import validate_data
from tokens.models import Token


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
    try:
        validate_data(owner, media_url)
    except ValueError as err:
        logging.error(err)
        return Response(
            {'message': f'{err}'},
            status=HTTPStatus.BAD_REQUEST
        )
    try:
        token_id = generate_token_id()
    except ValueError as err:
        logging.error(err)
        return Response(
            {'message': f'{err}'},
            status=HTTPStatus.BAD_REQUEST
        )
    txn = send_txn(
        create_txn(
            owner,
            token_id,
            media_url
        )
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
    paginator = CustomPagination()
    paginated_tokens = paginator.paginate_queryset(tokens, request)
    serializer = TokenSerializer(paginated_tokens, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
def get_total_supply(request):
    """
    Информация о текущем Total supply токена.
    Эндпоинт:
      * - tokens/total_supply/
    """
    return Response({'result': f'{get_supply()}'})
