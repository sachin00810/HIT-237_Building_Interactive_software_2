from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailOrUsernameBackend(ModelBackend):
    """
    Custom authentication backend that allows users to log in using either
    their username or their email address.

    This backend is registered in settings.AUTHENTICATION_BACKENDS and is
    called by Django's authenticate() pipeline before falling back to the
    default ModelBackend.

    Security note: email lookup is case-insensitive (email__iexact) to prevent
    account enumeration via case variations. The actual password check is
    delegated to the parent ModelBackend.check_password() which uses Django's
    constant-time comparison to prevent timing attacks.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()

        if username is None or password is None:
            return None

        # Determine whether the identifier is an email address
        if "@" in username:
            try:
                user = UserModel.objects.get(email__iexact=username)
            except UserModel.DoesNotExist:
                # Run the default password hasher to prevent timing attacks
                UserModel().set_password(password)
                return None
        else:
            try:
                user = UserModel.objects.get(username=username)
            except UserModel.DoesNotExist:
                UserModel().set_password(password)
                return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None
