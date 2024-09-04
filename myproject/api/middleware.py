from django.contrib.auth.models import AnonymousUser
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from knox.auth import TokenAuthentication
from urllib.parse import parse_qs

@database_sync_to_async
def get_user(token):
    auth = TokenAuthentication()
    try:
        user, auth_token = auth.authenticate_credentials(token.encode('utf-8'))
        return user
    except Exception:
        return AnonymousUser()

class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = parse_qs(scope['query_string'].decode())
        token = query_string.get('token', [None])[0]
        if token:
            scope['user'] = await get_user(token)
        else:
            scope['user'] = AnonymousUser()
        return await super().__call__(scope, receive, send)

def TokenAuthMiddlewareStack(inner):
    return TokenAuthMiddleware(inner)
