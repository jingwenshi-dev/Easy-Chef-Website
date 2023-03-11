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
    serializer_class = pass


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
