from django.shortcuts import render, redirect, reverse
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from allauth.socialaccount.views import SignupView
from allauth.account.views import PasswordSetView
from django.http import HttpResponseRedirect
from allauth.socialaccount.models import SocialLogin
from .models import User

"""
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created! You can login now')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})
"""

@login_required
def profile(request):
    is_socialaccount = False
    if request.user.socialaccount_set.filter(provider='google').exists():
        is_socialaccount = True
    return render(request, 'users/profile.html', {'is_socialaccount': is_socialaccount})

class CustomSocialSignupView(SignupView):
    def dispatch(self, request, *args, **kwargs):
        self.sociallogin = None
        data = request.session.get("socialaccount_sociallogin")
        if data:
            self.sociallogin = SocialLogin.deserialize(data)
        if not self.sociallogin:
            return HttpResponseRedirect(reverse("account_login"))
        user = self.sociallogin.user
        if (not user.id) and User.objects.filter(email=user.email).exists():
            messages.error(request, "There is another account with the email for this Google account. We currently do not allow linking this account to Google. Press 'Forgot password' if you forgot the password.")
            return redirect("/login/")
        return super(SignupView, self).dispatch(request, *args, **kwargs)