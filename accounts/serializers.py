from rest_framework.serializers import ModelSerializer
from .models import CustomUser

class SignupSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["username","password","email"]

class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
