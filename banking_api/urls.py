from django.urls import path

from .views.auth import AuthApi
from .views.users import UsersApi
from .views.belvo import BelvoTransactionsApi

urlpatterns = [
    path("auth/", AuthApi.as_view()),
    path("users/", UsersApi.as_view()),
    path("belvo/transactions/", BelvoTransactionsApi.as_view()),
]
