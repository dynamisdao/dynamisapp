from django.contrib.auth.decorators import (
    login_required,
    user_passes_test,
)

from authtools.views import DecoratorMixin


LoginRequired = DecoratorMixin(login_required)


def check_has_verified_keybase_username(user):
    return getattr(user, 'keybase_username', False)


KeybaseRequired = DecoratorMixin(user_passes_test(check_has_verified_keybase_username))


def check_user_is_admin(user):
    return user.is_authenticated() and user.is_admin


AdminRequired = DecoratorMixin(user_passes_test(check_user_is_admin))
