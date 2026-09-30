from rest_framework.routers import DefaultRouter

from practicodrf.views import NoteViewSet, TagViewSet

router = DefaultRouter()
router.register('notes', NoteViewSet, basename='note')
router.register('tags', TagViewSet, basename='tag')
