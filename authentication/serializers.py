from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        username = self.validated_data['username']
        email = self.validated_data['email']
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']

        if password != confirm_password:
            raise serializers.ValidationError({'password': 'As senhas não conferem.'})

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'Este e-mail já está em uso.'})

        user = User(username=username, email=email)
        user.set_password(password)
        user.save()

        Token.objects.create(user=user)

        return user