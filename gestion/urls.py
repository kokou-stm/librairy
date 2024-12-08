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
      path('meslivres/', meslivres, name='meslivres'),
      path('search/', search_book, name='search'),
      path('profile/', edit_profile, name='profile'),
      path('livre/<int:book_id>/', livre_detail, name='livre_detail'),
      path('livre/<int:book_id>/emprunter', emprunter_livre, name='emprunter_livre'),
]