from django.shortcuts import render, redirect
from rest_framework import viewsets
from .models import Note
from .serializers import NoteSerializer
import json

class NoteViewSet(viewsets.ModelViewSet):
    """API ViewSet untuk JSON responses"""
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


def note_list_html(request):
    """Function view untuk HTML rendering"""
    if request.method == 'POST':
        # Handle POST request
        title = request.POST.get('title')
        content = request.POST.get('content')
        Note.objects.create(title=title, content=content)
        return redirect('home')
    
    # Get all notes
    notes = Note.objects.all()
    
    # Serialize data untuk display
    serializer = NoteSerializer(notes, many=True)
    data_json = json.dumps(list(serializer.data), indent=4)
    
    context = {
        'notes': notes,
        'data': data_json,
    }
    
    return render(request, 'notes/note_list.html', context)