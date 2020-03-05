from django.contrib.auth.views import FormView
from django.contrib.auth import login

from users.forms import UserCreationForm


class RegisterView(FormView):
    form_class = UserCreationForm
    template_name = 'users/register.html'
    success_url = '/'
    success_message = f'Добро пожаловать на страницу Вашего профиля!'

    def form_valid(self, form):
        user = form.save()
        user.set_password(raw_password=form.cleaned_data['password1'])
        user.save()
        login(self.request, user)
        return super(RegisterView, self).form_valid(form)


