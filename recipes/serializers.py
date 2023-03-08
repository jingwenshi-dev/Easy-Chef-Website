from rest_framework import serializers

from recipes.models import Recipe, Ingredient, Step


class IngredientSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())

    class Meta:
        model = Ingredient
        fields = ['recipe', 'item', 'amount', 'unit']
        extra_kwargs = {
            'recipe': {'required': True},
            'item': {'required': True},
            'amount': {'required': True},
            'unit': {'required': True}
        }


class StepSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())

    class Meta:
        model = Step
        fields = ['recipe', 'description', 'picture']
        extra_kwargs = {
            'recipe': {'required': True},
            'description': {'required': True},
            'picture': {'required': True}
        }


class CreateRecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)
    steps = StepSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'picture', 'ingredients', 'steps', 'time', 'time_unit', 'cuisine', 'diet']
        extra_kwargs = {
            'title': {'required': True, 'max_length': 100},
            'description': {'required': True, 'max_length': 500},
            'picture': {'required': True},
            'ingredients': {'required': True},
            'steps': {'required': True},
            'time': {'required': True, 'max_length': 4},
            'time_unit': {'required': True, 'max_length': 5},
            'cuisine': {'required': True, 'max_length': 15},
            'diet': {'required': True, 'max_length': 30}
        }

    def create(self, validated_data):
        steps = validated_data.pop("steps")
        ingredients = validated_data.pop("ingredients")

        user = self.context['request'].user
        recipe = Recipe.objects.create(user=user, title=validated_data['title'],
                                       description=validated_data['description'],
                                       picture=validated_data['picture'], time=validated_data['time'],
                                       time_unit=validated_data['time_unit'], cuisine=validated_data['cuisine'],
                                       diet=validated_data['diet'])

        for step in steps:
            Step.objects.create(recipe=recipe, **step)

        for ingredient in ingredients:
            Ingredient.objects.create(recipe=recipe, **ingredient)

        return recipe
