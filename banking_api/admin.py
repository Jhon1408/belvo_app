from django.contrib import admin

from .models import Request
from .models import User
from .models import Auth

admin.site.register(Request)
admin.site.register(User)
admin.site.register(Auth)
