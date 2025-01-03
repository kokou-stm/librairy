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
       path('rendre/<int:emprunt_id>/', rendre_livre, name='rendre_livre'),
      path('verifier-emprunts/', verifier_emprunts, name='verifier_emprunts'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)