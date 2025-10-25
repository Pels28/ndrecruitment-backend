from .models import CustomUser
from rest_framework import serializers
from django.contrib.auth import authenticate

# base/serializers.py
from .models import CustomUser
from rest_framework import serializers
from django.contrib.auth import authenticate

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "email", "first_name", "last_name", "phone_number")
        
class UserRegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ("id", "email", "first_name", "last_name", "phone_number", "password1", "password2")
        extra_kwargs = {"password": {"write_only": True}}
        
    def validate(self, attrs):
        if not attrs.get("first_name"):
            raise serializers.ValidationError("First name is required")
        
        if not attrs.get("last_name"):
            raise serializers.ValidationError("Last name is required")
            
        if not attrs.get("phone_number"):
            raise serializers.ValidationError("Phone number is required")
            
        if not attrs.get("email"):
            raise serializers.ValidationError("Email is required")
        
        if attrs["password1"] != attrs["password2"]:
            raise serializers.ValidationError("Passwords do not match")
        
        password = attrs.get("password1", "")
        if len(password) < 8:
            raise serializers.ValidationError("Passwords must be at least 8 characters")
            
        return attrs
    
    def create(self, validated_data):
        password = validated_data.pop("password1")
        validated_data.pop("password2", None)
        
        user = CustomUser.objects.create_user(
            email=validated_data.get('email'),
            password=password,
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone_number=validated_data.get('phone_number', '')
        )
        
        return user
    
    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        # Authenticate using email as username
        try:
            user = CustomUser.objects.get(email=email)
            if user.check_password(password) and user.is_active:
                return user
        except CustomUser.DoesNotExist:
            pass
            
        raise serializers.ValidationError("Incorrect Credentials")