from enviroment.models import Enviroment
from django.core.exceptions import ImproperlyConfigured


def get_variable(name, default=None):
    try:
        type_mapping = {
            "int": int,
            "float": float,
            "bool": bool,
            "string": str,
        }

        variable = Enviroment.objects.get(name=name)

        if variable.type not in type_mapping:
            error_msg = "Variable type %s is not supported" % variable.type
            raise ImproperlyConfigured(error_msg)

        return type_mapping[variable.type](variable.value)

    except Enviroment.DoesNotExist:
        if default is not None:
            return default
        else:
            error_msg = "Set the %s enviroment variable" % name
            raise ImproperlyConfigured(error_msg)
