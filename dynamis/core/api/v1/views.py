from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from dynamis.core.api.v1.serializers import LoginSerializer


class LoginView(GenericAPIView):
    """
    A view for login user
    """
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            login(request, user)
            return Response(data={}, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(GenericAPIView):
    """
    A view for logout user
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(data={}, status=status.HTTP_200_OK)
