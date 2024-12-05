from django.urls import path
from .views import *
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index' ),
    path('login/', connection, name='login'),
    path('register/', register, name="register"),
    path('logout/', deconnexion, name='logout'),
      path('forgotpassword/', forgotpassword, name='forgotpassword'),
      path('code/', code, name='code'),
]