from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from .custom_auth import RawTokenAuthentication
from drf_yasg.utils import swagger_auto_schema
from .serializers import RegisterSerializer
from drf_yasg import openapi


class RegisterView(APIView):
    """
    Endpoint para registrar um novo usuário.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Cria um novo usuário e retorna um token de autenticação.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'email', 'password', 'confirm_password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, title='Nome de Usuário', description="Nome de usuário único para login."),
                'email': openapi.Schema(type=openapi.TYPE_STRING, title='E-mail', description="Endereço de e-mail válido."),
                'password': openapi.Schema(type=openapi.TYPE_STRING, title='Senha', format=openapi.FORMAT_PASSWORD, description="Senha forte com no mínimo 8 caracteres."),
                'confirm_password': openapi.Schema(type=openapi.TYPE_STRING, title='Confirmação de Senha', format=openapi.FORMAT_PASSWORD, description="Repita a senha inserida acima."),
            },
            example={
                "username": "joaosilva",
                "email": "joao.silva@example.com",
                "password": "Password@123",
                "confirm_password": "Password@123"
            }
        ),
        responses={
            201: openapi.Response(
                description="Usuário criado com sucesso.",
                examples={
                    "application/json": {
                        "user": {
                            "id": 1,
                            "username": "joaosilva",
                            "email": "joao.silva@example.com"
                        },
                        "token": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2"
                    }
                }
            ),
            400: "Requisição inválida (ex: senhas não conferem, e-mail já existe)."
        }
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.get(user=user).key
            data = {
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                },
                'token': token
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ValidateTokenView(APIView):
    """
    Endpoint para validar um token.
    """
    authentication_classes = [RawTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(status=status.HTTP_204_NO_CONTENT)

LoginView = ObtainAuthToken