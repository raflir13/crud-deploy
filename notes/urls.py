from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NoteViewSet, note_list_html

router = DefaultRouter()
router.register(r'notes', NoteViewSet, basename='note')

urlpatterns = [
    path('', include(router.urls)),
]