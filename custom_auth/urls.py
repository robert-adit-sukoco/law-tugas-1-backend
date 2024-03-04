from .views import *
from django.urls import path

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('check', UserView.as_view(), name='check_token')
]
