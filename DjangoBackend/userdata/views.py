from userdata.models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from userdata.serializers import *
from userdata.permissions import *

"""
API Class Naming Convention:
For API classes with more than one functionality of CRUD, use letters for shorthand.
E.g. RUDStepView is responsible for Retrieve, Update and Delete of a Step instance only.
"""


class CreateRatingView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RatingSerializer


class RURatingView(RetrieveUpdateAPIView):
    """
    A rating only need to be updated and must not be deleted
    """
    permission_classes = [IsAuthenticated, UserDataPermission]
    serializer_class = RatingSerializer

    def get_object(self):
        rtid = self.kwargs.get('rtid')
        rating = get_object_or_404(Rating, pk=rtid)
        return rating


class CreateCommentView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer


class RUDCommentView(RetrieveUpdateDestroyAPIView):
    """
    A comment can be updated, deleted and retrieved
    """
    permission_classes = [IsAuthenticated, UserDataPermission]
    serializer_class = CommentSerializer

    def get_object(self):
        cid = self.kwargs.get('cid')
        comment = get_object_or_404(Comment, pk=cid)
        return comment


class CreateLikedRecipeView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LikedRecipeSerializer


class RDLikedRecipeView(RetrieveDestroyAPIView):
    """
    A liked recipe can only be deleted
    """
    permission_classes = [IsAuthenticated, UserDataPermission]
    serializer_class = LikedRecipeSerializer

    def get_object(self):
        lrid = self.kwargs.get('lrid')
        liked_recipe = get_object_or_404(LikedRecipe, pk=lrid)
        return liked_recipe


class CreateBrowsedRecipeView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BrowsedRecipeSerializer


# Not sure if this class is needed
class RDBrowsedRecipeView(RetrieveDestroyAPIView):
    """
    A Browsed Recipe history can be deleted only
    """
    permission_classes = [IsAuthenticated, UserDataPermission]
    serializer_class = BrowsedRecipeSerializer

    def get_object(self):
        brid = self.kwargs.get('brid')
        browsed_recipe = get_object_or_404(BrowsedRecipe, pk=brid)
        return browsed_recipe

class CreateFavoritedRecipeView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FavoritedRecipeSerializer


class RDFavoritedRecipeView(RetrieveDestroyAPIView):
    """
    A liked recipe can only be deleted
    """
    permission_classes = [IsAuthenticated, UserDataPermission]
    serializer_class = FavoritedRecipeSerializer

    def get_object(self):
        frid = self.kwargs.get('frid')
        favorited_recipe = get_object_or_404(FavoritedRecipe, pk=frid)
        return favorited_recipe
    
class isFavoritedView(APIView):
    permission_classes = [IsAuthenticated, UserDataPermission]
    
    def get(self, request,  *args, **kwargs):
        rid = kwargs['rid']
        current_user = request.user
        recipe = get_object_or_404(Recipe, pk=rid)
        favorited = FavoritedRecipe.objects.filter(user=current_user, recipe=recipe)
        if favorited.exists():
            favoriteid = favorited.first().id
            return Response({"favorited": True, "frid": favoriteid})
        else:
            return Response({"favorited": False, "frid": None})


class CreateShoppingListView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ShoppingListSerializer


class RUDShoppingListView(RetrieveUpdateDestroyAPIView):
    """
    A shopping lst can be retrieved, updated, and deleted
    """
    permission_classes = [IsAuthenticated, UserDataPermission]
    serializer_class = ShoppingListSerializer

    def get_object(self):
        spid = self.kwargs.get('spid')
        shopping_lst = get_object_or_404(ShoppingList, pk=spid)
        return shopping_lst

class isInShoppingList(APIView):
    permission_classes = [IsAuthenticated, UserDataPermission]
    
    def get(self, request,  *args, **kwargs):
        rid = kwargs['rid']
        current_user = request.user
        recipe = get_object_or_404(Recipe, pk=rid)
        shoppinglist = ShoppingList.objects.filter(user=current_user, recipe=recipe)
        if shoppinglist.exists():
            shoppinglistid = shoppinglist.first().id
            return Response({"inshopping": True, "spid": shoppinglistid})
        else:
            return Response({"inshopping": False, "spid": None})

class allShoppingList(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ShoppingListSerializer

    def get_queryset(self):
        current_user = self.request.user
        shoppinglist = ShoppingList.objects.filter(user=current_user)
        return shoppinglist
    
    def get(self, request):
        shoppinglist = self.get_queryset()
        serializer = self.serializer_class(shoppinglist, many=True)
        return Response(serializer.data)