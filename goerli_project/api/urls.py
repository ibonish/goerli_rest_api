from django.urls import path
from api.views import create_token, get_list_tokens, get_total_supply


urlpatterns = [
    path('create/', create_token),
    path('list/', get_list_tokens),
    path('total_supply/', get_total_supply),
]
