from channels.auth import AuthMiddlewareStack
#from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from oauth2_provider.models import AccessToken

class TokenAuthMiddleware:
    """
    Token authorization middleware for Django Channels 2
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        headers = dict(scope['headers'])

        if b'sec-websocket-protocol' in headers:
                sec = headers[b'sec-websocket-protocol']
                values = sec.decode().split(',')
                if(len(values) != 2):
                    raise Exception("Error 101")

                try:
                    sent_access_token = values[1].strip()
                    token = AccessToken.objects.select_related("user").get(token=sent_access_token)
                    scope['user'] = token.user
                    print("user")
                    print(token.user)
                    close_old_connections()
                except AccessToken.DoesNotExist:
                    scope['user'] = AnonymousUser()


        """
        if b'authorization' in headers:
            try:
                token_name, token_key = headers[b'authorization'].decode().split()
                if token_name == 'Token':
                    token = Token.objects.get(key=token_key)
                    scope['user'] = token.user
                    close_old_connections()
            except Token.DoesNotExist:
                scope['user'] = AnonymousUser()
        """
        return self.inner(scope)

TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))