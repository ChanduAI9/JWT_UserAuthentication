from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from rest_framework.permissions import AllowAny
import os
from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .models import UserToken
from django.utils import timezone

def register(request):
    return render(request, 'frontend/register.html')

def login(request):
    return render(request, 'frontend/login.html')

def home(request):
    return render(request, 'frontend/home.html')

@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.create_user(username=username, password=password)
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@method_decorator(csrf_exempt, name='dispatch')
class CustomTokenObtainPairView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username=username).first()

        if user and user.check_password(password):
            user_token = UserToken.objects.filter(user=user).first()

            if user_token and user_token.access_token_expiration > timezone.now():
                self.log_login(user.username, user_token.access_token)
                return Response({
                    'access': user_token.access_token,
                    'refresh': user_token.refresh_token,
                }, status=status.HTTP_200_OK)

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            access_token_expiration = timezone.now() + timezone.timedelta(minutes=60)
            refresh_token_expiration = timezone.now() + timezone.timedelta(days=1)

            if user_token:
                user_token.access_token = access_token
                user_token.refresh_token = refresh_token
                user_token.access_token_expiration = access_token_expiration
                user_token.refresh_token_expiration = refresh_token_expiration
                user_token.save()
            else:
                UserToken.objects.create(
                    user=user,
                    access_token=access_token,
                    refresh_token=refresh_token,
                    access_token_expiration=access_token_expiration,
                    refresh_token_expiration=refresh_token_expiration
                )

            self.log_login(user.username, access_token)

            return Response({
                'refresh': refresh_token,
                'access': access_token,
            }, status=status.HTTP_200_OK)

        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    def log_login(self, username, access_token):
        """Logs the login time and access token to the tokens.log file."""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_path = os.path.join(os.path.dirname(__file__), 'tokens.log')

        # login time and token
        with open(file_path, 'a') as file:
            file.write(f"Time: {current_time}\n")
            file.write(f"Username: {username}\n")
            file.write(f"Access Token: {access_token}\n")
            file.write(f"{'-'*40}\n")