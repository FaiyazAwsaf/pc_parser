from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User
from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    EmailVerificationSerializer,
    ResendVerificationSerializer,
    UserProfileSerializer
)
from .utils import send_verification_email, send_welcome_email

class HelloView(APIView):
    def get(self, request):
        return Response({"message": "Hello from Django!"})

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Generate and send verification token
            token = user.generate_email_verification_token()
            
            # Send verification email
            email_sent = send_verification_email(user, token)
            
            return Response({
                'message': 'User registered successfully. Please check your email for verification code.',
                'email': user.email,
                'email_sent': email_sent
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Check if email is verified
            if not user.is_email_verified:
                return Response({
                    'error': 'Email not verified. Please verify your email before logging in.',
                    'email': user.email
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            
            return Response({
                'message': 'Login successful',
                'access_token': str(access_token),
                'refresh_token': str(refresh),
                'user': UserProfileSerializer(user, context={'request': request}).data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmailVerificationView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            token = serializer.validated_data['token']
            
            try:
                user = User.objects.get(email=email)
                
                if user.is_email_verified:
                    return Response({
                        'error': 'Email is already verified.'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                if user.verify_email_token(token):
                    # Send welcome email
                    send_welcome_email(user)
                    
                    return Response({
                        'message': 'Email verified successfully. You can now log in.',
                        'email': user.email
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'error': 'Invalid or expired verification code.'
                    }, status=status.HTTP_400_BAD_REQUEST)
                    
            except User.DoesNotExist:
                return Response({
                    'error': 'User with this email does not exist.'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResendVerificationView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = ResendVerificationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            try:
                user = User.objects.get(email=email)
                
                # Generate new token
                token = user.generate_email_verification_token()
                
                # Send verification email
                email_sent = send_verification_email(user, token)
                
                return Response({
                    'message': 'Verification code sent successfully.',
                    'email': user.email,
                    'email_sent': email_sent
                }, status=status.HTTP_200_OK)
                
            except User.DoesNotExist:
                return Response({
                    'error': 'User with this email does not exist.'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserProfileSerializer(request.user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Profile updated successfully',
                'user': serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            return Response({
                'message': 'Logout successful'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': 'Invalid token'
            }, status=status.HTTP_400_BAD_REQUEST)
