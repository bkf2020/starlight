from allauth.account.forms import ResetPasswordForm, SignupForm
from allauth.account.adapter import get_adapter
from django.utils.translation import gettext_lazy as _
from allauth.account.utils import filter_users_by_email
from django.core.exceptions import ValidationError
from allauth.account import app_settings
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

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

class CustomSignupForm(SignupForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    captcha.error_messages = {'required': 'The Captcha is required.'}
    field_order = [
        "username",
        "email",
        "password1",
        "password2",
        "captcha"
    ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None