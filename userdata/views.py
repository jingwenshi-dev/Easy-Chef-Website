from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from userdata.serializers import *

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
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
    serializer_class = BrowsedRecipeSerializer

    def get_object(self):
        brid = self.kwargs.get('brid')
        browsed_recipe = get_object_or_404(BrowsedRecipe, pk=brid)
        return browsed_recipe


class CreateShoppingListView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ShoppingListSerializer


class RDShoppingListView(RetrieveDestroyAPIView):
    """
    A shopping lst can be retrieved, updated, and deleted
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ShoppingListSerializer

    def get_object(self):
        spid = self.kwargs.get('spid')
        shopping_lst = get_object_or_404(ShoppingList, pk=spid)
        return shopping_lst
