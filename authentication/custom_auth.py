from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

class RawTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        print(f"Token recebido no header: {auth_header}")

        if not auth_header:
            return None

        try:
            return self.authenticate_credentials(auth_header)
        except AuthenticationFailed as e:
            raise e
        except Exception:
            raise AuthenticationFailed('Token inválido ou mal formatado.')