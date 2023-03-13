from django.shortcuts import get_object_or_404
from rest_framework import serializers
from recipes.models import *


class RecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    likes = serializers.SerializerMethodField('get_likes', read_only=True)
    rating = serializers.SerializerMethodField('get_avg_rating', read_only=True)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'picture', 'time', 'time_unit', 'cuisine', 'diet', 'likes', 'rating']
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

    def update(self, instance, validated_data):
        instance.title = validated_data['title']
        instance.description = validated_data['description']
        instance.picture = validated_data['picture']
        instance.time = validated_data['time']
        instance.time_unit = validated_data['time_unit']
        instance.cuisine = validated_data['cuisine'],
        instance.diet = validated_data['diet']

        instance.save()

        return instance

    def get_likes(self, instance):
        return instance.liked.count()

    def get_avg_rating(self, instance):
        rating_queue = instance.rated.all()
        total_score = sum([rating.score for rating in rating_queue])
        count = instance.rated.count()
        if count == 0:
            return 0
        return total_score / count


class IngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Ingredient
        fields = ['id', 'name']
        extra_kwargs = {
            'name': {'required': True}
        }


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """
    Serializer for RecipeIngredient model.
    Be able to include all fields' of its FK when return
    """
    id = serializers.IntegerField(read_only=True)
    recipe = RecipeSerializer(read_only=True)
    ingredient = IngredientSerializer(read_only=True)

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'recipe', 'ingredient', 'amount', 'unit']
        extra_kwargs = {
            'amount': {'required': True},
            'unit': {'required': True}
        }

    def create(self, validated_data):
        """
        @param iid: Ingredient object id
        @param rid: Recipe object id
        @return: A RecipeIngredient object with passed in rid and iid
        """
        rid = self.context['view'].kwargs.get('rid')
        iid = self.context['view'].kwargs.get('iid')

        recipe = get_object_or_404(Recipe, pk=rid)
        ingredient = get_object_or_404(Ingredient, pk=iid)

        amount = validated_data['amount']
        unit = validated_data['unit']

        if RecipeIngredient.objects.filter(recipe=recipe, ingredient=ingredient).exists():
            raise serializers.ValidationError(
                {"detail": "The current combination of recipe and ingredient already exist ("
                           "Hint: Update or Destroy current object)."})

        recipe_ingredient, created = RecipeIngredient.objects.update_or_create(recipe=recipe, ingredient=ingredient,
                                                                               amount=amount, unit=unit)

        return recipe_ingredient

    def update(self, instance, validated_data):
        """
        Update all fields (i.e. ingredient, amount, unit) in RecipeIngredient except for rid since this is an entity
        set combined to a certain recipe.
        @param instance: RecipeIngredient object returned by get_object(self) from outer scope.
        @return: Updated RecipeIngredient instance
        """
        iid = self.context['view'].kwargs.get('iid')

        ingredient = get_object_or_404(Ingredient, pk=iid)

        instance.ingredient = ingredient
        instance.amount = validated_data["amount"]
        instance.unit = validated_data["unit"]

        instance.save()

        return instance


class StepSerializer(serializers.ModelSerializer):
    recipe = RecipeSerializer(read_only=True)

    class Meta:
        model = Step
        fields = ['recipe', 'number', 'description', 'picture']
        extra_kwargs = {
            'number': {'required': True},
            'description': {'required': True},
            'picture': {'required': True}
        }

    def create(self, validated_data):
        rid = self.context['view'].kwargs.get('rid')
        recipe = get_object_or_404(Recipe, pk=rid)
        step = Step.objects.create(recipe=recipe, number=validated_data["number"],
                                   description=validated_data["description"], picture=validated_data["picture"])
        return step

    def update(self, instance, validated_data):
        instance.number = validated_data["number"]
        instance.description = validated_data["description"]
        instance.picture = validated_data["picture"]

        instance.save()

        return instance
