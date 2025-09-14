from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('alexa/', views.alexa_data, name='alexa_data'),
]
