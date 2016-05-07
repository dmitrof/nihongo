from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    #template_name = 'nihongo_tutor/singlekanji.html'
    bk = '星'
    return render(request, 'nihongo_tutor/singlekanji.html', {
            'bigkanji': bk,
        })

# Create your views here.
