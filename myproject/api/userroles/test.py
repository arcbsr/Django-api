# myapp/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .permissions import IsAdminUser, IsStaffUser, IsAdminOrStaffUser, IsUserOnly
from response import ResponseSend

class AdminOnlyView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def get(self, request):
        return Response({"message": "Hello, Admin!"})


class StaffOnlyView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsStaffUser]

    def get(self, request):
        return Response({"message": "Hello, Staff!"})


class AdminOrStaffView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminOrStaffUser]

    def get(self, request):
        return Response({"message": "Hello, Admin or Staff!"})

class UserOnlyView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsUserOnly]

    def get(self, request):
        return Response(ResponseSend.sendMsg({
            "message": "Hello, User!"
        }))
        # return Response({"message": "Hello, User!"})