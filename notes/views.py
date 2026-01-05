from django.shortcuts import render, redirect
from django.http import JsonResponse
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


def health_check(request):
    """Healthcheck endpoint untuk Railway"""
    import sys
    try:
        # Test database connection
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return JsonResponse({
            'status': 'healthy',
            'database': 'connected',
            'python_version': sys.version,
            'django_version': import_module('django').__version__,
        })
    except Exception as e:
        import traceback
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e),
            'traceback': traceback.format_exc()
        }, status=500)


def simple_test(request):
    """Test endpoint tanpa database"""
    return JsonResponse({
        'status': 'ok',
        'message': 'Django is running!'
    })


from importlib import import_module