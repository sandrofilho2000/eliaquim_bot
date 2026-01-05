from django.contrib import admin

class BaseAdmin(admin.ModelAdmin):
    def user_has_permission(self, request, perm_codename):
        if request.user.has_perm(f"{self.model._meta.app_label}.{perm_codename}"):
            return True

        # Verifica se o usuário faz parte de um grupo que tem essa permissão
        for profile in request.user.profiles.all():
            if profile.permissions.filter(codename=perm_codename).exists():
                return True
        return False    

    def has_view_permission(self, request, obj=None):
        """ print("IS USER STAFF: ", request.user.is_staff)
        if request.user.is_staff:
            return True """
        
        if self.user_has_permission(request, "view_" + self.model._meta.model_name):
            return True
        
        for group in request.user.groups.all():
            if self.user_has_permission(request, "view_" + self.model._meta.model_name, group):
                return True
        
        return False

    def has_add_permission(self, request):
        return request.user.is_superuser or self.user_has_permission(request, "add_" + self.model._meta.model_name)

    def has_change_permission(self, request, obj=None):
        return request.user.groups.filter(name="gerentes").exists() or self.user_has_permission(request, "change_" + self.model._meta.model_name)

    def has_delete_permission(self, request, obj=None):
        return self.user_has_permission(request, "delete_" + self.model._meta.model_name)