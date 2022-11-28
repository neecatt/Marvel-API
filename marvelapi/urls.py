from django.urls import path
from . import views

urlpatterns = [
    # path('', views.get_char_database, name='index'),
    path('seed', views.seed_characters, name='index'),
    path('get', views.get_from_marvel, name='index')
]   