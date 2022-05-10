from django.shortcuts import get_object_or_404
from rest_framework import viewsets


from reviews.models import Review, Comment, Title
from .serializers import ReviewSerializer, CommentSerializer
from .permissions import (
    ReadOnly, IsAuthor, IsModer, IsAdmin)

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class =  ReviewSerializer
    permission_classes = [ReadOnly|IsAuthor|IsModer|IsAdmin]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class =  CommentSerializer
    permission_classes =  [ReadOnly|IsAuthor|IsModer|IsAdmin]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = get_object_or_404(title.reviews, id=self.kwargs.get('review_id'))
        return review.comments

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = get_object_or_404(title.reviews, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, title=title, review=review)