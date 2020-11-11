from django.urls import path

from .views import HomePage


app_name = 'ShowStats'
urlpatterns = [
    path('', HomePage.as_view(), name='HomePage'),
]