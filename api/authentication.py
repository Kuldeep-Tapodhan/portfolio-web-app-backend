from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.exceptions import AuthenticationFailed

class SafeJWTAuthentication(JWTAuthentication):
    """
    Custom JWT Authentication class that fails gracefully.
    If the token is invalid or expired, it returns None (AnonymousUser)
    instead of raising a 401 Unauthorized error.
    This allows public endpoints to remain accessible even if the client
    sends a stale token.
    """
    def authenticate(self, request):
        try:
            return super().authenticate(request)
        except (InvalidToken, TokenError, AuthenticationFailed):
            return None
