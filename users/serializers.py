from  rest_framework import serializers 
from django.contrib.auth import get_user_model 

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username', 'email', 'password']
    def validate(self, data):
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')

        if not username or not password:
            raise Exception('username and email is required')
        if not password or len(password) < 6:
            raise Exception('password should have at least 6 characters')
        data['username'] = username
        data['email'] = email
        data['password'] = password
        return data 

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)