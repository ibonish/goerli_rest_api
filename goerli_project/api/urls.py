from django.urls import path

from api.views import create_token, get_token_list, get_total_supply

urlpatterns = [
    path('create/', create_token),
    path('list/', get_token_list),
    path('total_supply/', get_total_supply),
]
