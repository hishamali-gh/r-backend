from django.contrib.auth import authenticate, get_user_model
from django.db.models import Q
from rest_framework import serializers

User = get_user_model()

class RegistrationModelSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'is_staff', 'is_superuser', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError('Your password inputs do not match')
        
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')

        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField(max_length=30)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        identifier = attrs.get('identifier')
        password = attrs.get('password')

        user_obj = User.objects.filter(
            Q(username=identifier) | Q(email=identifier)
        ).first()

        if not user_obj:
            raise serializers.ValidationError('Invalid credentials')

        user = authenticate(
            username=user_obj.username,
            password=password
        )

        if not user:
            raise serializers.ValidationError('Invalid credentials')

        if not user.is_active:
            raise serializers.ValidationError('User account is disabled')

        attrs['user'] = user
        
        return attrs
