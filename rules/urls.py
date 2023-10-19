from django.urls import path

from .views import *

urlpatterns = [
    path('', rules, name='index'),
    path('rules/', rules, name='rules'),
    path('rule/<int:id>/', rule, name='rule'),
    path('description/', description, name='description'),
]