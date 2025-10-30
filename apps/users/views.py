
""" ========== Imports =========== """

from rest_framework import generics, permissions
from .models import User
from .serializers import UserSerializer

""" ========== CRUD Views =========== """

class UserListCreateAPIView(generics.ListCreateAPIView):
    """
    get:
     List all registered users.

    post:
     Create a new user account.
    """
    queryset = User.objects.all().order_by('-created_at')
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
     Retrieve a specific user's details by ID.

    put:
     Update an existing user's information.

    delete:
     Delete a user from the system.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
