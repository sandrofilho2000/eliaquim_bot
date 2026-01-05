from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Informações Pessoais'), {'fields': ('first_name', 'last_name', 'username')}),
        (_('Permissões'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'profiles', 'user_permissions')}),
        (_('Datas Importantes'), {'fields': ('last_login', 'date_joined')}),
    )
    filter_horizontal = ('groups', 'user_permissions', 'profiles')

    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'get_profiles')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'profiles')
    ordering = ('email', 'username', 'date_joined')

    def get_profiles(self, obj):
        return ", ".join([profile.name for profile in obj.profiles.all()])
    get_profiles.short_description = _('Perfis')