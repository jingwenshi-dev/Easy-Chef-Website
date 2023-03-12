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

    class Meta:
        model = Comment
        fields = ['id', 'user', 'recipe', 'message']
        extra_kwargs = {
            'message': {'required': True}
        }

    def create(self, validated_data):
        rid = self.context['view'].kwargs.get('rid')

        current_user = self.context['request'].user
        recipe = get_object_or_404(Recipe, pk=rid)
        message = validated_data['message']

        comment = Comment.objects.create(user=current_user, recipe=recipe, message=message)

        return comment

    def update(self, instance, validated_data):
        instance.message = validated_data['message']
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

        favorited_recipe = FavoritedRecipe.objects.create(user=current_user, recipe=recipe)

        return favorited_recipe


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
        fields = ['id', 'user', 'recipe']

    def create(self, validated_data):
        rid = self.context['view'].kwargs.get('rid')

        current_user = self.context['request'].user
        recipe = get_object_or_404(Recipe, pk=rid)

        if ShoppingList.objects.filter(user=current_user, recipe=recipe).exists():
            raise serializers.ValidationError(
                {"detail": "The current user has already add this recipe to the shopping list."})
        shopping_lst = ShoppingList.objects.create(user=current_user, recipe=recipe)

        return shopping_lst
