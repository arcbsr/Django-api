import json
from django.shortcuts import render, redirect
from ..apimodules.Room import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from knox.auth import TokenAuthentication
from knox.models import AuthToken
from rest_framework.exceptions import AuthenticationFailed

def CreateRoom(request):

    if request.method == 'POST':
        username = request.POST['username']
        room = request.POST['room']

        try:
            get_room = Room.objects.get(room_name=room)
            return redirect('room', room_name=room, username=username)

        except Room.DoesNotExist:
            new_room = Room(room_name = room)
            new_room.save()
            return redirect('room', room_name=room, username=username)

    return render(request, 'index.html')

def MessageView2(request, room_name, username):
    get_room = Room.objects.get(room_name=room_name)

    if request.method == 'POST':
        message = request.POST['message']

        print(message)

        new_message = Message(room=get_room, sender=username, message=message)
        new_message.save()
    get_messages= Message.objects.filter(room=get_room)
    print(get_messages)
    context = {
        "messages": get_messages,
        "user": username,
        "room_name": room_name,
    }
    return render(request, 'msg.html', context)


@csrf_exempt
def MessageView(request, room_name, username):
    try:
        get_room = Room.objects.get(room_name=room_name)
    except Room.DoesNotExist:
        return JsonResponse({'error': 'Room does not exist'}, status=404)

    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message', '')

        if not message:
            return JsonResponse({'error': 'Message content is required'}, status=400)

        new_message = Message(room=get_room, sender=username, message=message)
        new_message.save()

        return JsonResponse({
            'message': 'Message sent successfully',
            'message_id': new_message.id,
            'sender': username,
            'room_name': room_name,
            'content': message
        }, status=201)

    elif request.method == 'GET':
        get_messages = Message.objects.filter(room=get_room).order_by('timestamp')
        messages_list = [
            {'sender': msg.sender, 'message': msg.message, 'timestamp': msg.timestamp}
            for msg in get_messages
        ]

        return JsonResponse({
            'room_name': room_name,
            'messages': messages_list
        }, status=200)

    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)



def MessageViewauth(request, room_name, username):
    token_key  = request.GET.get('token')
    print(token_key)
    if not token_key:
        return JsonResponse({"error": "Token is required"}, status=401)
    
    try:
        token = AuthToken.objects.get(token_key= token_key)
        print(token)
    except AuthToken.DoesNotExist:
        return JsonResponse({"error": "Invalid token"}, status=401)
    user = token.user
    print(user)
    if user.username != username:
        return JsonResponse({"error": "Unauthorized"}, status=401)
    
    try:
        get_room = Room.objects.get(room_name=room_name)
    except Room.DoesNotExist:
        return JsonResponse({"error": "Room not found"}, status=404)

    if request.method == 'POST':
        message = request.POST['message']
        if message:
            new_message = Message(room=get_room, sender=username, message=message)
            new_message.save()
        else:
            return JsonResponse({"error": "Message content is required"}, status=400)

    get_messages = Message.objects.filter(room=get_room)
    context = {
        "messages": get_messages,
        "user": username,
        "room_name": room_name,
    }
    return render(request, 'msg.html', context)

from django.shortcuts import render, HttpResponse
from django.views import View
from django.contrib.auth.models import User
from knox.auth import TokenAuthentication
from knox.models import AuthToken
from rest_framework.exceptions import AuthenticationFailed

# def dashboard_view(request):
#     # Extract token from query parameters or headers
#     token_key = request.GET.get('token')
    
#     if not token_key:
#         return JsonResponse({"error": "Token is required"}, status=401)
    
#     try:
#         # Authenticate the token using Knox with the `digest` field
#         token = AuthToken.objects.get(digest=token_key)
#         user = token.user
#     except AuthToken.DoesNotExist:
#         return JsonResponse({"error": "Invalid token"}, status=401)
    
#     # Render the dashboard page with user information
#     context = {
#         "username": user.username,
#     }
#     return render(request, 'dashboard.html', context)

class DashboardView(View):
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        # Extract the token from the Authorization header
        token = request.headers.get('Authorization', None)
        # token_key = request.GET.get('token')
        print(token)
        if token and token.startswith('Token '):
            token = token.split('Token ')[1]

            # Authenticate the token
            user, auth_token = self.authenticate_token(token)
            if user:
                try:
                    get_room = Room.objects.get(room_name='fifa')
                except Room.DoesNotExist:
                    return JsonResponse({"error": "Room not found"}, status=404)

                if request.method == 'POST':
                    message = request.POST['message']
                    if message:
                        new_message = Message(room=get_room, sender=user, message=message)
                        new_message.save()
                    else:
                        return JsonResponse({"error": "Message content is required"}, status=400)

                get_messages = Message.objects.filter(room=get_room)
                context = {
                    "messages": get_messages,
                    "user": user.username,
                    "room_name": 'fifa',
                    "token": token,
                }
                return render(request, 'msg.html', context)
            else:
                return render(request, 'login.html', status=401)
        else:
            return render(request, 'login.html', status=401)

    def authenticate_token(self, token):
        try:
            # Knox's TokenAuthentication returns (user, auth_token) if the token is valid
            user, auth_token = TokenAuthentication().authenticate_credentials(token.encode())
            return user, auth_token
        except AuthenticationFailed:
            return None, None

