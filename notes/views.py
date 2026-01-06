from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
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

class NoteViewSet(viewsets.ModelViewSet):
    """API ViewSet untuk JSON responses"""
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


def note_list_html(request):
    """Function view untuk HTML rendering dengan CRUD lengkap"""
    
    # Handle UPDATE via AJAX (PUT request simulation dengan POST + _method)
    if request.method == 'POST' and request.POST.get('_method') == 'PUT':
        note_id = request.POST.get('id')
        note = get_object_or_404(Note, id=note_id)
        note.title = request.POST.get('title')
        note.content = request.POST.get('content')
        note.save()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': 'Note updated'})
        return redirect('notes')
    
    # Handle DELETE via AJAX (DELETE request simulation dengan POST + _method)
    if request.method == 'POST' and request.POST.get('_method') == 'DELETE':
        note_id = request.POST.get('id')
        note = get_object_or_404(Note, id=note_id)
        note.delete()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': 'Note deleted'})
        return redirect('notes')
    
    # Handle CREATE (POST)
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        Note.objects.create(title=title, content=content)
        return redirect('notes')
    
    # Handle READ (GET)
    notes = Note.objects.all().order_by('-created_at')
    
    context = {
        'notes': notes,
    }
    
    return render(request, 'notes/note_list.html', context)


def simple_test(request):
    """Test endpoint tanpa database"""
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"=== SIMPLE TEST CALLED ===")
    logger.info(f"Method: {request.method}")
    logger.info(f"Path: {request.path}")
    logger.info(f"Headers: {dict(request.headers)}")
    
    return JsonResponse({
        'status': 'ok',
        'message': 'Django is running!',
        'method': request.method,
        'path': request.path,
        'host': request.get_host(),
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