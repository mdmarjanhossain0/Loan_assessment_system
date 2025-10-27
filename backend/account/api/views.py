from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import GenericAPIView, UpdateAPIView
from django.contrib.auth import authenticate
from django.db import IntegrityError

from account.models import Account
from account.api.serializers import (
    LoginSerializer,
    RegistrationSerializer,
    AccountPropertiesSerializer,
    ChangePasswordSerializer
)
from account.api.utils import get_tokens
from mysite.constants import SUCCESS, ERROR

from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken
)

class RegisterView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                account = serializer.save()
                tokens = get_tokens(account)
                data = AccountPropertiesSerializer(account).data
                data["tokens"] = tokens

                return Response({
                    "response": SUCCESS,
                    "message": "User registered successfully.",
                    "data": data
                }, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({
                    "response": ERROR,
                    "error_message": "A user with this email or username already exists."
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView):
    permission_classes = [AllowAny]

    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data.get("email", "").lower().strip()
        password = request.data.get("password", "").strip()

        if not email or not password:
            return Response({
                "response": ERROR,
                "error_message": "Email and password are required."
            }, status=status.HTTP_400_BAD_REQUEST)

        account = authenticate(email=email, password=password)
        if not account:
            return Response({
                "response": ERROR,
                "error_message": "Invalid email or password."
            }, status=status.HTTP_401_UNAUTHORIZED)

        tokens = get_tokens(account)
        data = AccountPropertiesSerializer(account).data
        data["tokens"] = tokens

        return Response({
            "response": SUCCESS,
            "message": "User logged in successfully.",
            "data": data
        }, status=status.HTTP_200_OK)

class AccountDetailView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountPropertiesSerializer

    def get(self, request):
        serializer = self.get_serializer(request.user)
        return Response({
            "response": SUCCESS,
            "data": serializer.data
        }, status=status.HTTP_200_OK)


class AccountUpdateView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountPropertiesSerializer

    def put(self, request):
        serializer = self.get_serializer(
            request.user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response({
                "response": SUCCESS,
                "message": "Account updated successfully.",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.validated_data.get("old_password")
            new_password = serializer.validated_data.get("new_password")
            confirm_new_password = serializer.validated_data.get("confirm_new_password")

            if not user.check_password(old_password):
                return Response({"old_password": ["Incorrect password."]},
                                status=status.HTTP_400_BAD_REQUEST)

            if new_password != confirm_new_password:
                return Response({"new_password": ["New passwords must match."]},
                                status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()

            return Response({
                "response": SUCCESS,
                "message": "Password changed successfully."
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = None
    
    def get_serializer(self, *args, **kwargs):
        return None

    def post(self, request):
        try:
            tokens = OutstandingToken.objects.filter(user=request.user)
            for token in tokens:
                BlacklistedToken.objects.get_or_create(token=token)
            return Response({
                "response": SUCCESS,
                "message": "User logged out successfully. Tokens blacklisted."
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "response": ERROR,
                "error_message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
