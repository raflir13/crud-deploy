from django.http import HttpResponse
from django.urls import path

def test(request):
    return HttpResponse("OK DEPLOY BERHASIL")

urlpatterns = [
    path('', test),
]
