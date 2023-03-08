from rest_framework import serializers

from recipes.models import Recipe


class IngredientSerializer(serializers.ModelSerializer):
    pass


class StepSerializer(serializers.ModelSerializer):
    pass


class CreateRecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)
    steps = StepSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ['user', 'title', 'description', 'ingredients', 'steps', 'time', 'cuisine', 'diet']
