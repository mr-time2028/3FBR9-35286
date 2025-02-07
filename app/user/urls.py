from django.urls import path

from . import views


app_name = 'user'
urlpatterns = [
    path('register/', views.RegistrationApiView.as_view(), name='register'),
    path('login/', views.LoginApiView.as_view(), name='login'),
]
