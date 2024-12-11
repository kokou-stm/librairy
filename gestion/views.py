from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib import messages
import datetime
from datetime import timedelta

from django.db.models import Q
from django.core.mail import EmailMessage
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from .models import *
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def index(request):
    books = Book.objects.all()
    print(books)
    return render(request, "index.html", {"books":books})

@login_required
def meslivres(request):
    # Récupérer les emprunts de l'utilisateur connecté
    emprunts = Emprunts.objects.filter(id_membre__user=request.user).order_by('-date_emprunt')
    print(emprunts)
    return render(request, 'meslivres.html', {'emprunts': emprunts})


def livre_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    context = {'book': book}
    return render(request, "livre_detail.html", context)

@login_required
def emprunter_livre(request, book_id):
    # Récupérer le livre et le membre connecté
    book = get_object_or_404(Book, id=book_id)
    membre = get_object_or_404(Membre, user=request.user)

    # Vérifier si l'utilisateur a déjà emprunté ce livre sans le rendre
    if Emprunts.objects.filter(id_membre=membre, id_livre=book, status='C').exists():
        messages.error(request, "Vous avez déjà emprunté ce livre.")
        return redirect('livre_detail', book_id=book_id)

    # Créer un nouvel emprunt
    emprunt = Emprunts.objects.create(
        id_membre=membre,
        id_livre=book,
        status='C',  # Statut par défaut : en cours
        date_emprunt= datetime.date.today(),
        date_retour=(datetime.date.today() + timedelta(days=35))
    )
    emprunt.date_retour = emprunt.date_emprunt + datetime.timedelta(days=10)
    # Ajouter un message de succès et rediriger
    messages.success(request, "Le livre a été emprunté avec succès ! Retrouvez le dans vos emprunts.")
    return redirect('index')


from django.http import JsonResponse
from datetime import date
from .models import Emprunts

def verifier_emprunts(request):
    # Récupérer tous les emprunts en cours où la date de retour est dépassée
    emprunts_expires = Emprunts.objects.filter(
        status='C',
        date_retour__lt=date.today()
    )
    
    # Envoyer un e-mail à chaque utilisateur pour les emprunts expirés
    for emprunt in emprunts_expires:
        diff_jours = (date.today() - emprunt.date_retour).days
        message = f"Bonjour {emprunt.id_membre.nom},\n\n"
        message += f"Le livre '{emprunt.id_livre.titre}' devait être rendu le {emprunt.date_retour}.\n"
        message+= f"Vous etes en retard de {diff_jours} jours\n"
        message += "Nous sommes dans l'obligation de vous appliquer des pénalités supplémentaires selon le reglement de la bibliotheque."
        print("Emprunts: ", emprunt, diff_jours)

        if emprunt.penalite < (diff_jours//10)*5:
        # Envoi d'e-mail
            email = EmailMessage("Rappel : Date de retour dépassée",
                                message,
                                f"BU INSA Hauts-de-France <{settings.EMAIL_HOST}>",
                                [emprunt.id_membre.email])

            email.send()
        if diff_jours > 0: 
            emprunt.penalite = (diff_jours//10)*5
            emprunt.save()
    
    # Retourner les données pour JavaScript (si besoin d'afficher un statut)
    return JsonResponse({"message": "Rappels envoyés", "count": emprunts_expires.count()})


@login_required
def rendre_livre(request, emprunt_id):
    # Récupérer le livre et le membre connecté
    emprunt = get_object_or_404(Emprunts, id=emprunt_id)
    
    # Vérifier si l'utilisateur a déjà emprunté ce livre sans le rendre
    emprunt.delete()
    messages.error(request, "Le livre est rendu avec succes !.")
    return redirect('meslivres')

   

def search_book(request):
    query = request.GET.get('q', '')
    results = []
    
    if query:
        books = Book.objects.filter(titre__icontains=query)
        results = [{"id": book.id, "text": f"{book.titre} - {book.auteur}"} for book in books]
    
    return JsonResponse({"results": results})

def forgotpassword(request):
    return render(request, "index.html")


def register(request):
    mess = ""
    if request.method == "POST":
        
        print("="*5, "NEW REGISTRATION", "="*5)
        username = request.POST.get("username", None)
        email = request.POST.get("email", None)
        pass1 = request.POST.get("password1", None)
        pass2 = request.POST.get("password2", None)
        print(username, email, pass1, pass2)
        try:
            validate_email(email)
        except:
            mess = "Invalid Email"
        if pass1 != pass2 :
            mess += " Password not match"
        if User.objects.filter(Q(email= email)| Q(username=username)).first():
            mess += f" Exist user with email {email}"
        print("Message: ", mess)
        if mess=="":
            try:
                    validate_password(pass1)
                    user = User(username= username, email = email)
                    user.save()
                    user.password = pass1
                    user.set_password(user.password)
                    user.save()
                    subject= "Bienvenue à la bibliothèque de l'INSA Hauts-de-France ! "
                    email_message = f"""

                    Bonjour {username},

                    Félicitations et bienvenue à l'INSA Hauts-de-France ! 
                    Nous sommes ravis de vous compter parmi nos nouveaux étudiants et de vous accueillir à la bibliothèque.

                    Grâce à votre inscription, vous avez désormais accès à une large gamme de ressources pour accompagner vos études :

                    Des livres, des manuels, des revues et des articles scientifiques en libre accès.
                    Un espace de travail calme et adapté pour vos révisions.
                    Des services numériques, avec des bases de données en ligne, des e-books et bien plus encore.
                    Des ateliers et des événements pour vous aider à développer vos compétences en recherche documentaire et en gestion de l'information.

                    Votre carte d'étudiant vous permet également d'accéder aux services suivants :

                    Emprunt de documents et prolongation de prêts.
                    Accès à des espaces de travail collaboratif.
                    Réservation de salles de travail en groupe.

                    Pour plus d'informations sur nos horaires, nos services ou pour toute question, n'hésitez pas à consulter notre site web ou à nous contacter directement par e-mail ou téléphone.

                    Nous vous invitons à venir découvrir l'ensemble de nos services et à vous inscrire aux ateliers proposés pour optimiser vos recherches.

                    Nous vous souhaitons une excellente année universitaire et restons à votre disposition pour toute demande.

                    À très bientôt à la bibliothèque !

                    Cordialement,
                    L'équipe de la bibliothèque de l'INSA Hauts-de-France
                    03 27 51 77 47
                    https://bu.uphf.fr/opac/.do

                    """
                    email = EmailMessage(subject,
                             email_message,
                             f"BU INSA Hauts-de-France <{settings.EMAIL_HOST}>",
                             [user.email])

                    email.send()
                    mess = f"Welcome, {user.username}! Your account has been successfully created. To activate your account, please retrieve your verification code from the email sent to {user.email}"
                        
                    messages.info(request, mess)

                    verification_code, created = VerificationCode.objects.get_or_create(user=user)
                    verification_code.generate_code()
                    print(verification_code.code)
                    
                    code = EmailMessage('Votre code de vérification',
                             f'Votre code de vérification est : {verification_code.code}',
                             f"BU INSA Hauts-de-France <{settings.EMAIL_HOST}>",
                             [user.email])

                    code.send()
                    Membre.objects.create(user=user, email=email, nom= username ).save()
                    return redirect("code")
            except Exception as e:
                    print("error: ", e)
                    #err = " ".join(e)
                    messages.error(request, e)
                    return render(request, template_name="register.html")
            
        #messages.info(request, "Bonjour")

    return render(request, template_name="register.html")


def connection(request):
    mess = ""

    '''if request.user.is_authenticated:
         return redirect("dashboard")'''
    if request.method == "POST":
        
        print("="*5, "NEW CONECTION", "="*5)
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        try:
            validate_email(email)
        except:
            mess = "Invalid Email !!!"
        #authen = User.lo
        if mess=="":
            user = User.objects.filter(email= email).first()
            if user:
                auth_user= authenticate(username= user.username, password= password)
                if auth_user:
                    print("Utilisateur infos: ", auth_user.username, auth_user.email)
                    login(request, auth_user)
                    
                    return redirect("index")
                else :
                    mess = "Incorrect password"
            else:
                mess = "user does not exist"
            
        messages.info(request, mess)

    return render(request, template_name="login.html")

@login_required
def edit_profile(request):
    membre = get_object_or_404(Membre, user=request.user)
    
    if request.method == 'POST':
        # Récupérer les données du formulaire
        membre.phone = request.POST.get('phone', membre.phone)
        membre.numero_de_carte = request.POST.get('numero_de_carte', membre.numero_de_carte)
        
        # Sauvegarder les modifications
        membre.save()
        return redirect('index')  # Redirige vers la page du profil (ou une autre page)

    return render(request, 'profile.html', {'membre': membre})

def code(request):
    mess = ""

   
    if request.method == "POST":
        
        print("="*5, "NEW CONECTION", "="*5)
        email = request.POST.get("email")
        code_v = request.POST.get("code")
        user = User.objects.filter(email= email).first()
        verification_code, created = VerificationCode.objects.get_or_create(user=user)
        
        print(verification_code.code)
        if str(code_v) == str(verification_code.code) :
            messages.info(request, "Votre compte est activé . Connectez vous!")
            return redirect("login")
        else:
            mess = "Invalid code !!!"
      
        messages.info(request, mess)

    return render(request, template_name="code.html")



def deconnexion(request):
         print("Deconnexion")
         logout(request)
         return redirect("index")
    


