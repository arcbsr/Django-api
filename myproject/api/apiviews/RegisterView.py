# api/views.py

from rest_framework import generics
from rest_framework.response import Response
from knox.models import AuthToken
from rest_framework  import serializers
from ..apiserializers.serializers import UserSerializer, LoginSerializer
from ..models import CustomUser
from rest_framework import status

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.set_password(request.data['password'])
        user.save()
        _, token = AuthToken.objects.create(user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token
        })