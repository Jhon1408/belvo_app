import datetime as dt
import jwt

from django.conf import settings
from banking_api.models.auth import Auth
from banking_api.models.user import User


class TokenHandler:
    """Controls all the token functionalities for sessions"""

    def get_payload(self, request):
        """Returns token payload if is enabled or active."""
        header = request.headers.get("Authorization", None)
        if (
            not header
            or len(header.split(" ")) != 2
            or header.split(" ")[0].lower() != "bearer"
        ):
            return None, None

        try:
            token = jwt.decode(
                header.split(" ")[1], settings.SECRET_KEY, algorithms=["HS256"]
            )
        except jwt.InvalidTokenError:
            return None, None

        expiration_date = dt.datetime.strptime(
            token["expiration_date"], "%Y-%m-%d %H:%M:%S.%f"
        )

        db_token = Auth.objects.filter(token=header.split(" ")[1]).first()

        if expiration_date < dt.datetime.now() or not db_token or db_token.is_disabled:
            return None, None

        user = User.objects.filter(email=token["email"]).first()

        if not user or not user.is_active:
            return None, None

        return token, user
