from django import forms
from users.models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(max_length=30, label="Пароль", widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=30, label="Подтверждение пароля", widget=forms.PasswordInput())
    birthday = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
                               label='Дата рождения',
                               required=False)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name', 'birthday', ]

    def is_valid(self):
        return (super().is_valid() and (self.cleaned_data.get('password1') == self.cleaned_data.get('password2')))



