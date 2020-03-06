from django.shortcuts import redirect
from django.views.generic.base import View
from django.contrib.auth.views import FormView
from django.contrib.auth import login
from django.contrib import messages
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site

from users.forms import UserCreationForm
from users.models import User
from users.tokens import account_activation_token
from users.tasks import send_confirm_email


class RegisterView(FormView):
    form_class = UserCreationForm
    template_name = 'users/register.html'
    success_url = '/'
    success_message = f'Добро пожаловать на страницу Вашего профиля!'

    def form_valid(self, form):
        user = form.save()
        user.set_password(raw_password=form.cleaned_data['password1'])
        user.is_active = False
        user.save()
        domain = get_current_site(self.request).domain
        send_confirm_email(domain, user.pk)
        return super(RegisterView, self).form_valid(form)


class ActivateView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            messages.add_message(self.request, message='Регистрация подтверждена', level=messages.INFO)
            return redirect('home')
        else:
            messages.add_message(self.request, message='Регистрация не подтверждена', level=messages.INFO)
            return redirect('home')


