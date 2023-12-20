from django.shortcuts import render, redirect
from . import web
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import article
from django.core.cache import cache
import datetime

# Create your views here.
def index(request) :

    if request.method == 'POST':
        recherche = request.POST.get('recherche', '')
        # Vérifier si un titre de recherche est fourni
        if recherche:
            # Effectuer une requête pour récupérer les articles contenant le mot recherché dans leur titre
            articles_recherche = article.objects.filter(Title__icontains=recherche)
            articles = [
                {
                    "Title": art.Title,
                    "URL": art.URL,
                    "Paragraph": art.Paragraph,
                    "Image_URL": art.Image_URL,
                    "Date": art.Date
                }
                for art in articles_recherche
            ]
            return render(request, 'newsApp/recherche.html', {'articles': articles})

        # Vérifier si la ligne de code a déjà été exécutée aujourd'hui
        today = datetime.date.today().strftime('%Y-%m-%d')
        cache_key = 'web_main_executed_{}'.format(today)
        web_main_executed = cache.get(cache_key)
        if not web_main_executed:
            # Exécuter la ligne de code une fois par jour
            web.main()
            cache.set(cache_key, True, 86400)  # Marquer l'exécution de web.main() pour aujourd'hui

    articles_queryset = article.objects.all()  # Récupère tous les articles de la base de données
    # Convertir le queryset en une liste de dictionnaires
    articles = [
        {
            "Title": art.Title,
            "URL": art.URL,
            "Paragraph": art.Paragraph,
            "Image_URL": art.Image_URL,
            "Date": art.Date
        }
        for art in articles_queryset
    ]
    return render(request, 'newsApp/index.html', {'articles': articles})


def register(request) :

    if request.method == 'POST' :
        username = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2 :
            if User.objects.filter(email=email).exists() :
                messages.info(request, 'email already exists')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'username already exists')
                return redirect('register')
            else :
                user = User.objects.create_user(username=username,
                                                email = email,
                                                password=password)
                user.save()
                return redirect('login')
        else :
            messages.info(request, 'passwords not matching')
            return redirect('register')
        return redirect('/')
    else :
        return render(request,'newsApp/register.html')

def login(request) :
    if request.method == 'POST' :
        username = request.POST['name']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None :
            auth.login(request, user)
            return redirect('loginIndex')
        else :
            messages.info(request,'Invalid Credentials')
            return redirect('login')
    else :
        return render(request,'newsApp/login.html')

def loginIndex(request) :

    if request.method == 'POST':
        recherche = request.POST.get('recherche', '')
        # Vérifier si un titre de recherche est fourni
        if recherche:
            # Effectuer une requête pour récupérer les articles contenant le mot recherché dans leur titre
            articles_recherche = article.objects.filter(Title__icontains=recherche)
            articles = [
                {
                    "Title": art.Title,
                    "URL": art.URL,
                    "Paragraph": art.Paragraph,
                    "Image_URL": art.Image_URL,
                    "Date": art.Date
                }
                for art in articles_recherche
            ]
            return render(request, 'newsApp/recherche.html', {'articles': articles})

    articles_queryset = article.objects.all()  # Récupère tous les articles de la base de données
    # Convertir le queryset en une liste de dictionnaires
    articles = [
        {
            "Title": art.Title,
            "URL": art.URL,
            "Paragraph": art.Paragraph,
            "Image_URL": art.Image_URL,
            "Date": art.Date
        }
        for art in articles_queryset
    ]
    return render(request,'newsApp/loginIndex.html',{'articles' : articles})

def logout(request) :
    auth.logout(request)
    return redirect('/')


