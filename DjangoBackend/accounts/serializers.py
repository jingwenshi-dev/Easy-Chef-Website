from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])

    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password2', 'phone', 'avatar']
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
            'password': {'required': True, 'min_length': 8},
            'password2': {'required': True, 'min_length': 8},
            'phone': {'required': False},
            'avatar': {'required': False}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields do not match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

    def update(self, instance, validated_data):
        instance.username = validated_data['username']
        instance.email = validated_data['email']
        instance.phone = validated_data.get('phone')
        instance.avatar = validated_data.get('avatar')

        instance.set_password(validated_data['password'])
        instance.save()
        return instance
