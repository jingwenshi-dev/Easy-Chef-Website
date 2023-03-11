from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView, \
    RetrieveUpdateDestroyAPIView


# Create your views here.


class CreateRatingView(CreateAPIView):
    # TODO
    pass


class RURatingView(RetrieveUpdateAPIView):
    """
    A rating only need to be updated and must not be deleted
    """
    # TODO
    pass


class CreateCommentView(CreateAPIView):
    # TODO
    pass


class RUDCommentView(RetrieveUpdateDestroyAPIView):
    """
    A comment can be updated, deleted and retrieved
    """
    # TODO
    pass


class CreateLikedRecipeView(CreateAPIView):
    # TODO
    pass


class RDLikedRecipeView(RetrieveDestroyAPIView):
    """
    A liked recipe can only be deleted
    """
    # TODO
    pass


class CreateBrowsedRecipeView(CreateAPIView):
    # TODO
    pass


# Not sure if this class is needed
class DeleteBrowsedRecipeView(RetrieveDestroyAPIView):
    """
    A Browsed Recipe history can be deleted only
    """
    # TODO
    pass


class CreateShoppingListView(CreateAPIView):
    # TODO
    pass


class RUDShoppingListView(RetrieveUpdateDestroyAPIView):
    """
    A shopping lst can be retrieved, updated, and deleted
    """
    # TODO
    pass
