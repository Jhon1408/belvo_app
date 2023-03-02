import re

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from cerberus import Validator

from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

from django.core.cache import cache

from banking_api.helpers.paginator import paginate_content
from banking_api.helpers.token import TokenHandler
from banking_api.helpers.belvo_api import BelvoAPI

from banking_api.models.user import User


class BelvoTransactionsApi(APIView, TokenHandler):
    """The APIView for the Belvo Api helper"""

    def get(self, request, *args, **kwargs):
        """Get all transactions of a user"""
        payload, user = self.get_payload(request)
        if not payload:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return Response(
                {
                    "code": "unauthorized",
                    "detailed": "Your user is not active",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        validator = Validator(
            {
                "refresh": {
                    "type": "string",
                    "required": False,
                    "allowed": ["true", "false"],
                }
            }
        )

        if not validator.validate(request.GET):
            return Response(
                {
                    "code": "invalid_request",
                    "detailed": "Invalid request",
                    "errors": validator.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not request.GET.get("refresh") or not bool(request.GET["refresh"]):
            if cache.get(f"transactions_{user.email}_{user.role}"):
                return Response(
                    {
                        "code": "transactions_found",
                        "detailed": "User transactions retrieved successfully",
                        "data": cache.get(f"transactions_{user.email}_{user.role}"),
                    },
                    status=status.HTTP_200_OK,
                )

        belvo_api = BelvoAPI()
        owner = belvo_api.get_all_owners(filters={"email": user.email})["results"]
        if not owner:
            return Response(
                {
                    "code": "no_owner_found",
                    "detailed": "Your user is not an owner",
                },
                status=status.HTTP_200_OK,
            )
        try:
            owner_link = owner[0]["link"]
        except KeyError:
            return Response(
                {
                    "code": "no_owner_link_found",
                    "detailed": "Your user has no link",
                },
                status=status.HTTP_200_OK,
            )

        user_accounts = belvo_api.get_all_accounts(filters={"link": owner_link})[
            "results"
        ]
        if not user_accounts:
            return Response(
                {
                    "code": "no_accounts_found",
                    "detailed": "No accounts found",
                },
                status=status.HTTP_200_OK,
            )

        accounts_ids = [account["id"] for account in user_accounts if "id" in account]
        accounts_links = [
            account["link"] for account in user_accounts if "link" in account
        ]
        user_transactions = []

        for account_id, account_link in zip(accounts_ids, accounts_links):
            user_transactions += belvo_api.get_all_transactions(
                filters={"link": account_link, "account": account_id}
            )["results"]
        if not user_transactions:
            return Response(
                {
                    "code": "no_transactions_found",
                    "detailed": "No transactions found",
                },
                status=status.HTTP_200_OK,
            )

        cache.set(
            f"transactions_{user.email}_{user.role}",
            user_transactions,
            timeout=60 * 60 * 24,
        )

        return Response(
            {
                "code": "transactions_found",
                "detailed": "User transactions retrieved successfully",
                "data": user_transactions,
            },
            status=status.HTTP_200_OK,
        )
