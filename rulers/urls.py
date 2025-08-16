from django.urls import path
from rulers import views

urlpatterns = [
    path('', views.home, name='home'),
]