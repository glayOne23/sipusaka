"""Module"""
from apps.landingpage.views import home
from django.urls import path

app_name = 'landingpage'

urlpatterns = [
  path('',      home.home,       name='home'),
#   path('404',   home.error_404,  name='404')
]