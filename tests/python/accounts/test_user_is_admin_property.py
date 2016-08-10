def test_user_is_admin_if_superuser(user):
    user.is_superuser = True
    user.is_staff = False
    user.save()

    assert user.is_superuser and not user.is_staff
    assert user.is_admin


def test_user_is_admin_if_staff(user):
    user.is_superuser = False
    user.is_staff = True
    user.save()

    assert not user.is_superuser and user.is_staff
    assert user.is_admin


def test_user_is_admin_if_both_superuser_and_staff(user):
    user.is_superuser = True
    user.is_staff = True
    user.save()

    assert user.is_superuser and user.is_staff
    assert user.is_admin


def test_user_is_not_admin_if_neither_superuser_and_staff(user):
    user.is_superuser = False
    user.is_staff = False
    user.save()

    assert not user.is_superuser and not user.is_staff
    assert not user.is_admin
