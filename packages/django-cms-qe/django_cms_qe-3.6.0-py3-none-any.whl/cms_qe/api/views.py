from django.contrib.auth import get_user_model
from django.db.models import Model
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import AuthenticationFailed


class CmsQeBasicAuthentication(BasicAuthentication):

    def authenticate_credentials(self, userid: str, password: str, request: HttpRequest = None) -> tuple[Model, None]:
        """Check credentials against settings and return AnonymousUser or None."""
        class_user = get_user_model()
        try:
            user = class_user.objects.get(username=userid, is_active=True)
        except class_user.DoesNotExist as err:
            raise AuthenticationFailed(_("User inactive or deleted.")) from err
        if user.check_password(password):
            return (user, None)
        raise AuthenticationFailed(_("Invalid username/password."))
