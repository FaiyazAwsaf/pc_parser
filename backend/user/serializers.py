from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User
import re

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password', 'password_confirm', 'profile_image')
        
    def validate_email(self, value):
        """Validate email format and uniqueness"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        
        # Basic email validation
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, value):
            raise serializers.ValidationError("Enter a valid email address.")
        
        return value.lower()
    
    def validate_username(self, value):
        """Validate username format and uniqueness"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        
        # Username should be alphanumeric and underscores only
        if not re.match(r'^[a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError("Username can only contain letters, numbers, and underscores.")
        
        if len(value) < 3:
            raise serializers.ValidationError("Username must be at least 3 characters long.")
        
        return value
    
    def validate_first_name(self, value):
        """Validate first name"""
        if not value.strip():
            raise serializers.ValidationError("First name is required.")
        
        if not re.match(r'^[a-zA-Z\s]+$', value):
            raise serializers.ValidationError("First name can only contain letters and spaces.")
        
        return value.strip().title()
    
    def validate_last_name(self, value):
        """Validate last name"""
        if not value.strip():
            raise serializers.ValidationError("Last name is required.")
        
        if not re.match(r'^[a-zA-Z\s]+$', value):
            raise serializers.ValidationError("Last name can only contain letters and spaces.")
        
        return value.strip().title()
    
    def validate(self, attrs):
        """Validate password confirmation"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs
    
    def create(self, validated_data):
        """Create user with validated data"""
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError("Invalid email or password.")
            
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled.")
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError("Must include email and password.")

class EmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField(max_length=6, min_length=6)
    
    def validate_token(self, value):
        """Validate token format"""
        if not value.isdigit():
            raise serializers.ValidationError("Token must be a 6-digit number.")
        return value

class ResendVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate_email(self, value):
        """Check if user exists and is not already verified"""
        try:
            user = User.objects.get(email=value)
            if user.is_email_verified:
                raise serializers.ValidationError("Email is already verified.")
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        
        return value

class UserProfileSerializer(serializers.ModelSerializer):
    profile_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'is_email_verified', 'date_joined', 'profile_image', 'profile_image_url')
        read_only_fields = ('id', 'email', 'is_email_verified', 'date_joined', 'profile_image_url')
    
    def get_profile_image_url(self, obj):
        """Get the full URL for the profile image"""
        if obj.profile_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.profile_image.url)
            return obj.profile_image.url
        return None
