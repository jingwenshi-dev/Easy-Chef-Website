from django.shortcuts import get_object_or_404
from userdata.models import *
from accounts.serializers import *


class RatingSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Rating
        fields = ['id', 'user', 'recipe', 'score']
        extra_kwargs = {
            'score': {'required': True},
        }
