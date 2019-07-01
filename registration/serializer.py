from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('email', 'full_name', 'password', 'is_teacher', 'password_confirm', 'avatar')

    def validate(self, attrs):
        data = super(UserSerializer, self).validate(attrs)
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError('Password mismatch')
        del data['password_confirm']
        return data