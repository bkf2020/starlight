from allauth.account.forms import ResetPasswordForm
from allauth.account.adapter import get_adapter
from django.utils.translation import gettext_lazy as _
from allauth.account.utils import filter_users_by_email
from django.core.exceptions import ValidationError
from allauth.account import app_settings

class CustomResetPasswordForm(ResetPasswordForm):
    def clean_email(self):
        email = self.cleaned_data["email"]
        email = get_adapter().clean_email(email)
        self.users = filter_users_by_email(email)
        if not self.users and not app_settings.PREVENT_ENUMERATION:
            raise ValidationError(
                _("The email address is not assigned to any user account")
            )
        elif self.users[0].socialaccount_set.filter(provider='google').exists():
            raise ValidationError(
                _("Cannot reset password for sign in with Google account")
            )
        return self.cleaned_data["email"]