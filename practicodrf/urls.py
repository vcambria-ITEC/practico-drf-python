from django.urls import path

from . import views

urlpatterns = [
    path('', views.board_page, name='board-page'),
    path('login/', views.login_page, name='login-page'),
    path('register/', views.register_page, name='register-page'),
    path('api/register/', views.register, name='api-register'),
]
