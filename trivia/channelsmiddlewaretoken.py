from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser

# from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import AccessToken

@database_sync_to_async
def get_user(headers):
    print(headers[b'authorization'].decode().split())
    try:
        token_name, token_key = headers[b'authorization'].decode().split()
        print("Token Name", token_name, "Token Key", token_key)
        if token_name == 'Token':
            print("We at least got past the if")
            tokens = AccessToken.objects.all(key=token_)
            print(tokens)
            token = AccessToken.objects.get(token=token_key)
            print("Token", token)
            print("Token User", token.user)
            return token.user
    # except Token.DoesNotExist:
    except:
        print("We're hitting the except")
        return AnonymousUser()


class TokenAuthMiddleware:

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        return TokenAuthMiddlewareInstance(scope, self)


class TokenAuthMiddlewareInstance:
    """
    Yeah, this is black magic:
    https://github.com/django/channels/issues/1399
    """
    def __init__(self, scope, middleware):
        self.middleware = middleware
        self.scope = dict(scope)
        self.inner = self.middleware.inner

    async def __call__(self, receive, send):
        headers = dict(self.scope['headers'])
        if b'authorization' in headers:
            self.scope['user'] = await get_user(headers)
        inner = self.inner(self.scope)
        return await inner(receive, send)


TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))