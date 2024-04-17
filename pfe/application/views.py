from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UtilisateurForm

def login_view(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        login_form = LoginForm()
    return render(request, 'login.html', {'login_form': login_form})

def register_view(request):
    if request.method == 'POST':
        utilisateur_form = UtilisateurForm(request.POST)
        if utilisateur_form.is_valid():
            utilisateur = utilisateur_form.save()
            return redirect('login')
    else:
        utilisateur_form = UtilisateurForm()
    return render(request, 'register.html', {'utilisateur_form': utilisateur_form})


def essay1(request):
   return render(request,'acceuil.html')
def essay2(request):
   return render(request,'traitement_mansuel.html')
def essay3(request):
   return render(request,'traitm_p1.html')
def essay4(request):
   return render(request,'traitm_annuel.html')
def essay5(request):
   return render(request,'dashboard.html')
def essay6(request):
   return render(request,'login.html')
def essay7(request):
   return render(request,'creation_compt.html')

