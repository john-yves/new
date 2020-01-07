from django.urls import path, include
from .views import HomePageView
from . import views

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('password/',views.change_password,name='change_password')
]