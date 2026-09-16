from django.urls import path

from . import views

urlpatterns = [
    # Paginas HTML
    path('', views.board_page, name='board-page'),
    path('login/', views.login_page, name='login-page'),
    path('register/', views.register_page, name='register-page'),

    # API
    path('api/register/', views.register, name='api-register'),
    path('api/notes/', views.NoteListCreateView.as_view(), name='api-note-list'),
    path('api/notes/<int:pk>/', views.NoteDetailView.as_view(), name='api-note-detail'),
    path('api/tags/', views.TagListCreateView.as_view(), name='api-tag-list'),
    path('api/tags/<int:pk>/', views.TagDetailView.as_view(), name='api-tag-detail'),
]
