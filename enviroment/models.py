from django.db import models

ENV_VAR_TYPES = [
    ("string", "string"),
    ("int", "int"),
    ("float", "float"),
    ("bool", "bool"),
]


class Enviroment(models.Model):
    """Enviroment model"""

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=ENV_VAR_TYPES)
    value = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Enviroment Variable"
        verbose_name_plural = "Enviroment Variables"
        ordering = ["-created_at"]
