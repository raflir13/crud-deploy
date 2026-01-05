from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework import viewsets
from .models import Note
from .serializers import NoteSerializer
import json
import sys
from importlib import import_module
import traceback


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


def simple_test(request):
    """Test endpoint tanpa database"""
    return JsonResponse({
        'status': 'ok',
        'message': 'Django is running!',
        'method': request.method,
        'path': request.path,
    })


def health_check(request):
    """Healthcheck endpoint untuk Railway"""
    try:
        # Test database connection
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        import django
        
        return JsonResponse({
            'status': 'healthy',
            'database': 'connected',
            'python_version': sys.version.split()[0],
            'django_version': django.__version__,
        })
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e),
            'traceback': traceback.format_exc()
        }, status=500)