from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView as AuthLoginView
from django.conf import settings
from django.contrib.auth.decorators import login_required


class SignupFormView(CreateView):
    form_class = UserCreationForm
    template_name = 'accounts/signup_form.html'
    success_url = settings.LOGIN_URL

class LoginView(AuthLoginView):
    def get_template_names(self):
        if self.request.is_ajax():
            return ['accounts/_login.html']
        return ['accounts/login.html']


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')