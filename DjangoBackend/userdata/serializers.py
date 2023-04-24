from userdata.models import *
from recipes.serializers import *
from accounts.serializers import UserSerializer
from recipes.serializers import RecipeSerializer


class RatingSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = UserSerializer(read_only=True)
    recipe = RecipeSerializer(read_only=True)

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

        if Rating.objects.filter(user=current_user, recipe=recipe).exists():
            raise serializers.ValidationError({"detail": "The current user has already rated this recipe."})

        rating = Rating.objects.create(user=current_user, recipe=recipe, score=score)

        return rating

    def update(self, instance, validated_data):
        instance.score = validated_data["score"]
        instance.save()
        return instance


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = UserSerializer(read_only=True)
    recipe = RecipeSerializer(read_only=True)
    createdDate = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'recipe', 'message', 'file', 'createdDate']
        extra_kwargs = {
            'message': {'required': True},
            'file': {'required': False}
        }

    def create(self, validated_data):
        rid = self.context['view'].kwargs.get('rid')

        current_user = self.context['request'].user
        recipe = get_object_or_404(Recipe, pk=rid)
        message = validated_data['message']
        file = validated_data.get('file')

        if file:
            comment = Comment.objects.create(user=current_user, recipe=recipe, message=message, file=file)
        else:
            comment = Comment.objects.create(user=current_user, recipe=recipe, message=message)

        return comment

    def update(self, instance, validated_data):
        instance.message = validated_data['message']
        instance.file = validated_data.get('file')
        instance.save()
        return instance


class LikedRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = UserSerializer(read_only=True)
    recipe = RecipeSerializer(read_only=True)

    class Meta:
        model = LikedRecipe
        fields = ['id', 'user', 'recipe']

    def create(self, validated_data):
        rid = self.context['view'].kwargs.get('rid')

        current_user = self.context['request'].user
        recipe = get_object_or_404(Recipe, pk=rid)

        if LikedRecipe.objects.filter(user=current_user, recipe=recipe).exists():
            raise serializers.ValidationError({"detail": "The current user has already liked this recipe."})

        liked_recipe = LikedRecipe.objects.create(user=current_user, recipe=recipe)

        return liked_recipe


class FavoritedRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = UserSerializer(read_only=True)
    recipe = RecipeSerializer(read_only=True)

    class Meta:
        model = FavoritedRecipe
        fields = ['id', 'user', 'recipe']

    def create(self, validated_data):
        rid = self.context['view'].kwargs.get('rid')

        current_user = self.context['request'].user
        recipe = get_object_or_404(Recipe, pk=rid)

        if FavoritedRecipe.objects.filter(user=current_user, recipe=recipe).exists():
            raise serializers.ValidationError({"detail": "The current user has already favorited this recipe."})

        favourite_recipe = FavoritedRecipe.objects.create(user=current_user, recipe=recipe)

        return favourite_recipe


class BrowsedRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = UserSerializer(read_only=True)
    recipe = RecipeSerializer(read_only=True)

    class Meta:
        model = BrowsedRecipe
        fields = ['id', 'user', 'recipe']

    def create(self, validated_data):
        rid = self.context['view'].kwargs.get('rid')

        current_user = self.context['request'].user
        recipe = get_object_or_404(Recipe, pk=rid)

        if BrowsedRecipe.objects.filter(user=current_user, recipe=recipe).exists():
            raise serializers.ValidationError({"detail": "The current user has already browsed this recipe."})

        browsed_recipe = BrowsedRecipe.objects.create(user=current_user, recipe=recipe)

        return browsed_recipe


class ShoppingListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = UserSerializer(read_only=True)
    recipe = RecipeSerializer(read_only=True)

    class Meta:
        model = ShoppingList
        fields = ['id', 'user', 'recipe', 'number']
        

    def create(self, validated_data):
        rid = self.context['view'].kwargs.get('rid')

        current_user = self.context['request'].user
        recipe = get_object_or_404(Recipe, pk=rid)

        if ShoppingList.objects.filter(user=current_user, recipe=recipe).exists():
            raise serializers.ValidationError(
                {"detail": "The current user has already add this recipe to the shopping list."})
        shopping_lst = ShoppingList.objects.create(user=current_user, recipe=recipe)

        return shopping_lst

    def update(self, instance, validated_data):
        action = self.context['request'].query_params.get('action')
        if action == 'add':
            instance.number += 1
        if action == 'remove':
            instance.number -= 1
        instance.save()
        return instance