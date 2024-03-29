"""starlight URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.views.generic.base import RedirectView
from users import views as user_views
from allauth.account.views import LoginView
urlpatterns = [
    path('', user_views.root_page, name='root-page'),
    path('admin/', admin.site.urls),
    path('about/', include('about.urls')),
    path('problems/', include('problems.urls')),
    path('journal/', include('journal.urls')),
    path('import/', include('import.urls')),
    path('register/', RedirectView.as_view(url="/accounts/signup/"), name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('accounts/social/signup/', user_views.CustomSocialSignupView.as_view(), name='socialaccount_signup'),
    path('accounts/email/', RedirectView.as_view(url="/profile/"), name='account_email'),
    path('accounts/password/set/', RedirectView.as_view(url="/profile/"), name='account_set_password'),
    path('accounts/', include('allauth.urls'))
]
