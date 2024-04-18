from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd


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


def upload_file(request):
    if request.method == 'POST' and request.FILES['file'].name.endswith('.xlsx'):
        # read the data from the Excel file using pandas
        data = pd.read_excel(request.FILES['file'], engine='openpyxl')
        # convert the data to a Python list of dictionaries for use in the template
        data_list = data.to_dict('records')
        context = {'data': data_list}
        return render(request, 'upload.html', context)

    elif request.method == 'GET':
        return render(request, 'upload.html', {'data': None})

    else:
        return HttpResponse('Invalid file type. Please upload an Excel file.')