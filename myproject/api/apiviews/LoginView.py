
from rest_framework import generics
from rest_framework.response import Response
from knox.models import AuthToken
from rest_framework  import serializers
from ..apiserializers.serializers import UserSerializer, LoginSerializer
from ..models import CustomUser
from rest_framework import status
from response import ResponseSend
    
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token = AuthToken.objects.create(user=user)[1]
            return Response(ResponseSend.sendMsg({
                'token': token,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role,
                }
            }))
            # return Response({
            #     'token': token,
            #     'user': {
            #         'id': user.id,
            #         'username': user.username,
            #         'email': user.email,
            #     }
            # })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)