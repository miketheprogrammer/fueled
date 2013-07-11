def CustomAuthContext(request):
    return {
        'is_admin_user': bool(request.user.groups.filter(name="Administrator")),
        'is_standard_user': bool(request.user.groups.filter(name="Standard User")),
    }
