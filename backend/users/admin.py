from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Follow, User


class UserChangeForm(forms.ModelForm):

    class Meta:
        model = User
        fields = '__all__'


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    list_display = ('email', 'username', 'first_name', 'last_name', 'avatar')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'first_name',
                                      'last_name', 'avatar')}),
    )


admin.site.register(User, UserAdmin)
admin.site.register(Follow)
