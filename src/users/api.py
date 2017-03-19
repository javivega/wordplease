from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.permissions import UserPermission
from users.serializers import UserSerializer


class UsersAPI(APIView):

    permission_classes = (UserPermission,)

    def get(self, request):
        """
        Devuelve una lista de los usuarios del sistema
        :param request: HttpRequest
        :return: HttpResponse
        """

        users = User.objects.all()
        self.check_object_permissions(request, users)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Creacción de un usuario
        :param request: HttpRequest
        :return: HttpResponse
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailAPI(APIView):
    permission_classes = (UserPermission,)
    def get(self, request, pk):
        """User detail que consigue el detalle de un usuario lo puede actualizar y borrar"""
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        self.check_object_permissions(request, user)
        return Response(serializer.data)

    def put(self, request, pk):
        """Actualization de un usuario"""
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a user
        :param request: HttpRequest
        :param pk: User Primary key
        :return: Response
        """
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
