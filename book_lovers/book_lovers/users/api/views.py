from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from book_lovers.users.models import Profile
from .serializers import UserSerializer, ProfileSerializer
from book_lovers.users.permissions import IsStaffOrTargetUser


class UserViewSet(viewsets.ModelViewSet):
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = (IsStaffOrTargetUser,)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
