from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NoteViewSet, note_list_html

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
]