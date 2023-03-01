from django.db import models


class Request(models.Model):
    """Model to store the requests made by the app"""

    endpoint = models.CharField(max_length=255)
    method = models.CharField(max_length=255)
    data = models.JSONField(null=True, blank=True)
    response = models.JSONField()

    def __str__(self):
        return f"{self.method} {self.endpoint}"

    class Meta:
        verbose_name = "Request"
        verbose_name_plural = "Requests"
