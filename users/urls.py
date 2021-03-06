from django.urls import path
from django.contrib.auth.views import LoginView, logout_then_login
from users.views import RegisterView, ActivateView


urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', logout_then_login, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), name='activate'),
]