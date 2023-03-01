""" Contains the Auth model """

from django.db import models


class Auth(models.Model):
    """Authentication definition for sessions."""

    creation_date = models.DateTimeField(auto_now_add=True)
    is_disabled = models.BooleanField(default=False)
    token = models.TextField("Token", max_length=700)

    class Meta:
        verbose_name = "Authentication"
        verbose_name_plural = "Authentications"

    def __str__(self):
        return self.token
