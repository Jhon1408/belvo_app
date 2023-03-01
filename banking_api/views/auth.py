import datetime as dt
import jwt

from cerberus import Validator
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from banking_api.models.auth import Auth
from banking_api.models.user import User

from enviroment.helpers.get_variable import get_variable


class AuthApi(APIView):
    """Defines the HTTP verbs to auth model management."""

    def post(self, request):
        """Creates a new session."""
        validator = Validator(
            {
                "email": {"required": True, "type": "string"},
                "password": {"required": True, "type": "string", "minlength": 7},
                "keep_logged_in": {"required": True, "type": "boolean"},
                "role": {
                    "required": True,
                    "type": "string",
                    "allowed": ["user", "admin"],
                },
            }
        )
        if not validator.validate(request.data):
            return Response(
                {
                    "code": "invalid_body",
                    "detailed": "Invalid body",
                    "data": validator.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        obj = User.objects.filter(
            email=request.data["email"],
            role=request.data["role"],
        ).first()

        if not obj:
            return Response(
                {
                    "code": "user_not_found",
                    "detailed": f"User not found with email {request.data['email']}",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        if not check_password(request.data["password"], obj.password):
            return Response(
                {"code": "incorrect_password", "detailed": "Incorrect password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = get_random_string(30)
        token = jwt.encode(
            {
                "expiration_date": str(
                    dt.datetime.now()
                    + (
                        dt.timedelta(hours=get_variable("TOKEN_EXP_HOURS"))
                        if not request.data["keep_logged_in"]
                        else dt.timedelta(
                            days=get_variable("KEEP_LOGGED_IN_TOKEN_EXP_DAYS")
                        )
                    )
                ),
                "email": obj.email,
                "role": obj.role,
                "refresh": refresh,
            },
            settings.SECRET_KEY,
            algorithm="HS256",
        )

        User.objects.filter(email=obj.email).update(last_login=dt.datetime.now())
        Auth.objects.create(token=token)

        return Response(
            {
                "id": obj.pk,
                "token": token,
                "refresh": refresh,
                "email": obj.email,
                "username": obj.username,
                "role": obj.role,
            },
            status=status.HTTP_201_CREATED,
        )

    def patch(self, request):
        """Disables a session."""
        header = request.headers.get("Authorization", None)

        if (
            not header
            or len(header.split(" ")) != 2
            or header.split(" ")[0].lower() != "bearer"
        ):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        session = Auth.objects.filter(token=header.split(" ")[1])
        if not session:
            return Response(status=status.HTTP_404_NOT_FOUND)

        session.update(is_disabled=True)
        return Response(status=status.HTTP_200_OK)


class RefreshTokenApi(APIView):
    """Defines the HTTP verbs to refresh token."""

    def patch(self, request, *args, **kwargs):
        """Refreshes a token."""
        header = request.headers.get("Authorization", None)

        if (
            not header
            or len(header.split(" ")) != 2
            or header.split(" ")[0].lower() != "bearer"
        ):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            token = jwt.decode(header.split(" ")[1], settings.SECRET_KEY)
        except jwt.InvalidTokenError:
            return Response(
                {"code": "invalid_token", "detailed": "Invalid token"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if token["refresh"] != kwargs["refresh"]:
            return Response(
                {
                    "code": "do_not_have_permission",
                    "detailed": "You don't have permission to perform this action",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        obj = User.objects.filter(email=token["email"], role=token["role"]).first()
        if not obj:
            return Response(
                {
                    "code": "user_not_found",
                    "detailed": f"User not found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        refresh = get_random_string(30)
        token = jwt.encode(
            {
                "expiration_date": str(
                    (
                        dt.datetime.now()
                        + dt.timedelta(days=get_variable("TOKEN_EXP_DAYS"))
                    )
                ),
                "email": obj.email,
                "role": obj.role,
                "refresh": refresh,
            },
            settings.SECRET_KEY,
            algorithm="HS256",
        )

        session = Auth.objects.filter(token=header.split(" ")[1])
        if not session:
            return Response(
                {
                    "code": "token_not_found",
                    "detailed": "Token not found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        session.update(token=token)

        return Response(
            {
                "id": obj.pk,
                "token": token,
                "refresh": refresh,
                "email": obj.email,
                "username": obj.username,
                "role": obj.role,
            },
            status=status.HTTP_201_CREATED,
        )
