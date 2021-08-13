from django.contrib.auth import authenticate
from rest_framework import serializers


#TODO: register serializer
from account.models import CustomUser
from utils import send_activation_code


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only=True)
    password_confirm = serializers.CharField(min_length=6, write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'password_confirm')

    def validate(self, validated_data):     # def validate = def clean, validated_data = cleaned_data
        # {"password": "helloworld", "password_confirm": "helloworld", "email": "test@test.com"}
        password = validated_data.get('password')
        password_confirm = validated_data.get('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Пароли не совпадают')
        return validated_data

    def create(self, validated_data):
        """Эта функция вызыв когда мы сохраняем объект через self.save()"""
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = CustomUser.objects.create_user(email=email, password=password)
        send_activation_code(email=user.email, activation_code=user.activation_code)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        label='Password',
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)

            if not user:
                message = 'Вы не можете залогинется с предоставленными данными'
                raise serializers.ValidationError(message, code='authorization')

        else:
            message = "Должен включать 'email' и 'password'"
            raise serializers.ValidationError(message, code='authorization')
        attrs['user'] = user
        return attrs







