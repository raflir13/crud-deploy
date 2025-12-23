from django.shortcuts import render
from rest_framework import viewsets
from .models import Note
from .serializers import NoteSerializer

class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    
    
def item_list_view(request):
    items = Note.objects.all()
    return render(request, 'crud/index.html', {'items': items})