import re

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from cerberus import Validator

from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

from banking_api.helpers.paginator import paginate_content
from banking_api.helpers.token import TokenHandler

from banking_api.models.user import User

from banking_api.serializers.users import UserSerializer


class UsersApi(APIView, TokenHandler):
    """The APIView for the User model"""

    def post(self, request):
        """Creates a new user"""
        validator = Validator(
            {
                "email": {"required": True, "type": "string"},
                "username": {"required": True, "type": "string"},
                "password": {
                    "required": True,
                    "type": "string",
                    "regex": r"^.*(?=.{8,100})(?=.*[a-zA-Z])(?=.*[a-z])(?=.*\d)[a-zA-Z0-9].*$",
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

        request.data["email"] = request.data["email"].lower()
        request.data["password"] = make_password(request.data["password"])

        user = User.objects.filter(email=request.data["email"]).first()
        if user:
            return Response(
                {
                    "code": "integrity_error",
                    "detailed": f"User with email {request.data['email']} already exists",
                },
                status=status.HTTP_409_CONFLICT,
            )

        user = User.objects.create(**request.data)

        return Response(
            {
                "code": "user_created",
                "detailed": "User created successfully",
                "data": {"user": UserSerializer(user).data},
            },
            status=status.HTTP_201_CREATED,
        )

    @paginate_content()
    def get(self, request, *args, **kwargs):
        """Get all users"""
        payload, user = self.get_payload(request)
        if not payload:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if user.role != "admin":
            return Response(
                {
                    "code": "unauthorized",
                    "detailed": "You are not authorized to perform this action",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        users = User.objects.all()
        return Response(
            {
                "code": "users_found",
                "detailed": "Users retrieved successfully",
                "data": UserSerializer(users, many=True).data,
            },
            status=status.HTTP_200_OK,
        )
