from django.shortcuts import get_object_or_404
from rest_framework import serializers

from accounts.models import User
from recipes.models import Recipe, Ingredient, Step


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ['item', 'amount', 'unit']
        extra_kwargs = {
            'item': {'required': True},
            'amount': {'required': True},
            'unit': {'required': True}
        }

    def create(self, validated_data):
        rid = self.context['view'].kwargs.get('rid')
        recipe = get_object_or_404(Recipe, pk=rid)
        ingredient = Ingredient.objects.create(recipe=recipe, item="item", amount="amount", unit="unit")
        return ingredient


class StepSerializer(serializers.ModelSerializer):
    # recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())

    class Meta:
        model = Step
        fields = ['number', 'description', 'picture']
        extra_kwargs = {
            'number': {'required': True},
            'description': {'required': True},
            'picture': {'required': True}
        }

    def create(self, validated_data):
        rid = self.context['view'].kwargs.get('rid')
        recipe = get_object_or_404(Recipe, pk=rid)
        step = Step.objects.create(recipe=recipe, description="description", picture="picture")
        return step


class RecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'picture', 'time', 'time_unit', 'cuisine', 'diet']
        extra_kwargs = {
            'uid': {'required': True},
            'title': {'required': True, 'max_length': 100},
            'description': {'required': True, 'max_length': 500},
            'picture': {'required': True},
            'time': {'required': True, 'max_length': 4},
            'time_unit': {'required': True, 'max_length': 5},
            'cuisine': {'required': True, 'max_length': 15},
            'diet': {'required': True, 'max_length': 30}
        }

    def create(self, validated_data):
        current_user = self.context['request'].user
        recipe = Recipe.objects.create(user=current_user, title=validated_data['title'],
                                       description=validated_data['description'],
                                       picture=validated_data['picture'], time=validated_data['time'],
                                       time_unit=validated_data['time_unit'], cuisine=validated_data['cuisine'],
                                       diet=validated_data['diet'])

        return recipe
