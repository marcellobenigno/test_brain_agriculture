import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email='admin@email.com',
        password='demodemo',
        first_name='Admin',
        last_name='Admin',
    )


@pytest.fixture
def superuser(db):
    return User.objects.create_superuser(
        email='superadmin@email.com',
        password='demodemo'
    )


def test_user_exists(user):
    assert user is not None


def test_str(user):
    assert user.email == 'admin@email.com'


def test_return_attributes():
    fields = (
        'id',
        'email',
        'first_name',
        'last_name',
        'password',
        'is_active',
        'is_admin',
        'is_superuser',
        'date_joined',
        'last_login',
    )

    for field in fields:
        assert hasattr(User, field)


def test_user_is_authenticated(user):
    assert user.is_authenticated


def test_user_is_active(user):
    assert user.is_active


def test_user_is_staff(user):
    assert not user.is_staff


def test_user_is_superuser(user):
    assert not user.is_superuser


def test_superuser_is_superuser(superuser):
    assert superuser.is_superuser


def test_user_has_perm(user):
    assert callable(user.has_perm)


def test_user_has_module_perms(user):
    assert callable(user.has_module_perms)


def test_user_get_full_name(user):
    assert user.get_full_name() == 'Admin Admin'


def test_user_get_short_name(user):
    assert user.get_short_name() == 'Admin'
