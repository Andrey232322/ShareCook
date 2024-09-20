from django.contrib import admin
from .models import Subscription, User

# Register your models here.
admin.site.register(User)
admin.site.register(Subscription)
