""" from pages.models import Page, SubPage
def pages_for_sidebar(request):
    user = request.user
    all_pages = Page.objects.filter(active=True).prefetch_related("subpages")
    allowed_pages = []

    if user.is_superuser:
        allowed_pages = all_pages
    else:
        
        if user.is_anonymous:
            return {
                'sidebar_pages': [],
            }

        user_permissions = user.get_all_custom_permission_codenames()

        # DEBUG: Printar permissões
        print("PERMISSÕES DO USUÁRIO + PERFIL:")
        for perm in user_permissions:
            print(" -", perm)

        for page in all_pages:
            app_label = page.app_related
            has_permission = any(perm.startswith(f"{app_label}.") for perm in user_permissions)
            if has_permission:
                allowed_pages.append(page)

    return {
        'sidebar_pages': allowed_pages,
    }
 """