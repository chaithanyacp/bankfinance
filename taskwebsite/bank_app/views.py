from django.shortcuts import render

# Create your views here.
# from bank_app.models import Team


def index(request):
    return render(request,"index.html")