from django.shortcuts import render

from POSApp.models import POSDB


# Create your views here.
def index(request):
    print(POSDB.objects.all().values())
    return render(request, "index.html")

def test(request):
    return render(request, "index.html")