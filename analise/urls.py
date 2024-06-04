from django.urls import path
from . import views

urlpatterns = [
    path('', views.predict_acidente, name='predict_acidente'),
]