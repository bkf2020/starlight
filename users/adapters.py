from allauth.account.adapter import DefaultAccountAdapter
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.staticfiles.storage import staticfiles_storage

disposable_emails_loc = staticfiles_storage.path("domains.txt")
disposable_emails = set()
with open(disposable_emails_loc, "r") as disposable_emails_list:
    for domain in disposable_emails_list.readlines():
        disposable_emails.add(domain.strip())

class FilterEmailAccountAdapter(DefaultAccountAdapter):
    def clean_email(self, email):
        if email.split("@")[1].strip() in disposable_emails:
            raise ValidationError(_("We believe that email is disposable. Disposable emails are not allowed to prevent spam."))
        return super().clean_email(email)