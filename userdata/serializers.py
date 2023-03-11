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

    def create(self, validated_data):
        rid = self.context['view'].kwargs.get('rid')

        current_user = self.context['request'].user
        recipe = get_object_or_404(Recipe, pk=rid)
        score = validated_data['score']

        rating = Rating.objects.create(user=current_user, recipe=recipe, score=score)

        return rating

    def update(self, instance, validated_data):
        instance.score = validated_data["score"]
        instance.save()
        return instance
