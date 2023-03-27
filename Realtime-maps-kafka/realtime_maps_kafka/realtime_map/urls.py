# from telnetlib import LOGOUT
# from django.contrib import admin
from django.urls import path
from .views import *
# from .utils import *
# from django.contrib.auth import views as auth_views

# from django.conf import settings
# from django.conf.urls.static import static
# from django.contrib.auth.middleware import AuthenticationMiddleware


urlpatterns = [

    path('index', index, name="index"),
    path('consumer', stream, name="consumer"),
    path('data_pass', data_pass, name="data_pass"),
    path('delete_message', delete_message, name="delete_message"),
  


]
