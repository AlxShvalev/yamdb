from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User


class UserSignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value in ('me',):
            raise ValidationError(f'Username не может быть {value}')
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=60)
    confirmation_code = serializers.SlugField()


class AdminSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=60, required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise ValidationError(f'Пользователь {value} уже существует')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError(f'Пользователь с email {value},'
                                  ' уже существует')
        return value


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=60, required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        read_only_fields = ('role',)
