from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from accounts.serializers import RegisterSerializer


# Create your views here.
class SignUpView(CreateAPIView):
    queryset = User.objects.all()  # Declare the set of objects to operate on
    serializer_class = RegisterSerializer


class LogOutView(APIView):
    """
    Reference: https://medium.com/django-rest/logout-django-rest-framework-eb1b53ac6d35
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return JsonResponse({"Logout": True})
