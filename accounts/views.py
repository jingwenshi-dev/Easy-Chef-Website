from django.http import JsonResponse
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from accounts.models import User
from accounts.serializers import UserSerializer
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


# Create your views here.
class SignUpView(CreateAPIView):
    queryset = User.objects.all()  # Declare the set of objects to operate on
    serializer_class = UserSerializer


class LogOutView(APIView):
    """
    Reference: https://medium.com/django-rest/logout-django-rest-framework-eb1b53ac6d35
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # TODO
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_200_OK)


class RUProfileView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        user = self.request.user
        return user

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

