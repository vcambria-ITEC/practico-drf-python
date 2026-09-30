from django.shortcuts import render
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Note, Tag
from .serializers import NoteSerializer, RegisterSerializer, TagSerializer


class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    refresh = RefreshToken.for_user(user)
    return Response(
        {'refresh': str(refresh), 'access': str(refresh.access_token), 'username': user.username},
        status=status.HTTP_201_CREATED,
    )


def login_page(request):
    return render(request, 'practicodrf/login.html')


def register_page(request):
    return render(request, 'practicodrf/register.html')


def board_page(request):
    return render(request, 'practicodrf/board.html')
