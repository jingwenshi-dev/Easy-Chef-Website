from django.shortcuts import render
from rest_framework.generics import CreateAPIView

from accounts.models import User
from accounts.serializers import RegisterSerializer


# Create your views here.
class SignUpView(CreateAPIView):
    queryset = User.objects.all()  # Declare the set of objects to operate on
    serializer_class = RegisterSerializer

# class LogInView():
#     pass
