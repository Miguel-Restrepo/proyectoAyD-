from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, Template
from django.template import  loader
def inicio(request): #PRimera vista
   
    return render(request,'inicio.html')
def funcionParametroURL(request,p1): #PRimera vista
    documento="""<html>
    <body>
    <h1>
    se ingreso %s
    </h1>
    </body>
    </html>"""% p1
    return HttpResponse(documento)