from functools import wraps

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect


def login_required(view):
    """
    Custom login_required to handle ajax request
    Check user is login and is_active
    """
    @wraps(view)
    def inner(request, *args, **kwargs):
        if not request.user.is_authenticated() or not request.user.is_active:
            if request.is_ajax():
                # if is ajax return 403
                return JsonResponse({'login_url': settings.LOGIN_URL}, status=403)
            else:
                # if not ajax redirect login page
                return redirect(settings.LOGIN_URL)
        return view(request, *args, **kwargs)
    return inner


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **kwargs):
        return login_required(super().as_view(**kwargs))
