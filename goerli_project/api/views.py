from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET', 'POST'])
def create_token(request):
    if request.method == 'POST':
        return Response({'message': 'Получены данные', 'data': request.data})
    return Response({'message': 'Это был GET-запрос создание...!'})


@api_view(['GET', 'POST'])
def get_list_tokens(request):
    return Response({'message': 'Это был GET-запрос для листа!'})


@api_view(['GET', 'POST'])
def get_total_supply(request):
    return Response({'message': 'Это был GET-запрос для тотал саплая!'})
