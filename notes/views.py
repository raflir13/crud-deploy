from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from rest_framework import viewsets
from .models import Note
from .serializers import NoteSerializer
import sys
import traceback


class NoteViewSet(viewsets.ModelViewSet):
    """API ViewSet untuk JSON responses (optional, bisa dihapus jika tidak dipakai)"""
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


def note_list_html(request):
    """Function view untuk HTML rendering dengan CRUD lengkap"""
    
    # Handle UPDATE via POST + _method=PUT
    if request.method == 'POST' and request.POST.get('_method') == 'PUT':
        note_id = request.POST.get('id')
        note = get_object_or_404(Note, id=note_id)
        note.title = request.POST.get('title')
        note.content = request.POST.get('content')
        note.save()
        return redirect('notes')
    
    # Handle DELETE via POST + _method=DELETE
    if request.method == 'POST' and request.POST.get('_method') == 'DELETE':
        note_id = request.POST.get('id')
        note = get_object_or_404(Note, id=note_id)
        note.delete()
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