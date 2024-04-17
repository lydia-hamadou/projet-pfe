from django.shortcuts import render


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



