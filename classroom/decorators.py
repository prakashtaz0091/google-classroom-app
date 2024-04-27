from django.shortcuts import redirect
from django.contrib import messages


def has_to_be_teacher(func):
    def wrapper(request, *args, **kwargs):
        if request.user.profile.role == 'teacher':
            return func(request, *args, **kwargs)
        else:
            messages.error(request, "You don't have permissions to view that page")
            return redirect('classroom:home')
    return wrapper