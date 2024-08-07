def user_context(request):
    return {
        'user_name': request.user.username if request.user.is_authenticated else None,
    }
