from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password', 'date_of_birth']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            date_of_birth=validated_data['date_of_birth'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        username_or_email = data.get("username_or_email")
        password = data.get("password")

        # Try to authenticate by username or email
        user = authenticate(username=username_or_email, password=password)
        if user is None:
            user = authenticate(email=username_or_email, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid login credentials")
        
        data['user'] = user
        return data


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({
            'username': self.user.username,
            'email': self.user.email,
            'phone_number': self.user.phone_number
        })
        return data