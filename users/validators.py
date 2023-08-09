from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from better_profanity import profanity

def validate_profanity(username):
    if username != None and profanity.contains_profanity(username):
        raise ValidationError(_("We believe the specified username contains profanity."))

def validate_username_length(username):
    if len(username) > 35:
        raise ValidationError(_("The specified username is over 35 characters"))

custom_validators = [validate_profanity, validate_username_length, UnicodeUsernameValidator]