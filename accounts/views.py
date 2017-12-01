from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.conf import settings

class SignupFormView(CreateView):
    form_class = UserCreationForm
    template_name = 'accounts/signup_form.html'
    success_url = settings.LOGIN_URL