from django.shortcuts import redirect
from django.urls import reverse


EXEMPT_URLS = (
    '/accounts/2fa/verify/',
    '/accounts/logout/',
    '/accounts/login/',
    '/accounts/register/',
    '/admin/',
    '/static/',
    '/media/',
)


class TwoFactorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (
            request.user.is_authenticated
            and not request.session.get('2fa_verified')
            and not any(request.path.startswith(u) for u in EXEMPT_URLS)
        ):
            try:
                profile = request.user.profile
                if profile.two_factor_enabled:
                    return redirect(f"{reverse('accounts:verify_2fa')}?next={request.path}")
            except Exception:
                pass

        return self.get_response(request)
