from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from notes.models import LongReview, ShortReview
from .serializers import LongReviewSerializer, ShortReviewSerializer, LongReviewCommentSerializer
from .models import LongReviewLike, LongReviewComment, ShortReviewLike

class LongReviewListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LongReviewSerializer

    def get_queryset(self):
        return LongReview.objects.filter(open=True).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        request.id_list = list(queryset.values_list('id', flat=True))  # 리뷰 ID 목록을 설정
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class LongReviewDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LongReviewSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return LongReview.objects.filter(open=True).order_by('-created_at')

    def get_object(self):
        queryset = self.get_queryset()
        review_id_list = list(queryset.values_list('id', flat=True))
        lookup_value = self.kwargs[self.lookup_field]
        actual_id = review_id_list[int(lookup_value) - 1]
        return get_object_or_404(LongReview, id=actual_id, open=True)

class ShortReviewListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ShortReviewSerializer

    def get_queryset(self):
        return ShortReview.objects.filter(open=True).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        request.id_list = list(queryset.values_list('id', flat=True))  # 리뷰 ID 목록을 설정
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class ShortReviewDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ShortReviewSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return ShortReview.objects.filter(open=True).order_by('-created_at')

    def get_object(self):
        queryset = self.get_queryset()
        review_id_list = list(queryset.values_list('id', flat=True))
        lookup_value = self.kwargs[self.lookup_field]
        actual_id = review_id_list[int(lookup_value) - 1]
        return get_object_or_404(ShortReview, id=actual_id, open=True)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def long_review_like(request, id):
    queryset = LongReview.objects.filter(open=True).order_by('-created_at')
    review_id_list = list(queryset.values_list('id', flat=True))
    actual_id = review_id_list[int(id) - 1]
    review = get_object_or_404(LongReview, id=actual_id, open=True)
    user = request.user
    if LongReviewLike.objects.filter(review=review, user=user).exists():
        LongReviewLike.objects.filter(review=review, user=user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        LongReviewLike.objects.create(review=review, user=user)
        return Response(status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def long_review_comment(request, id):
    queryset = LongReview.objects.filter(open=True).order_by('-created_at')
    review_id_list = list(queryset.values_list('id', flat=True))
    actual_id = review_id_list[int(id) - 1]
    review = get_object_or_404(LongReview, id=actual_id, open=True)
    user = request.user
    comment_text = request.data.get('comment')
    if comment_text:
        comment = LongReviewComment.objects.create(review=review, user=user, comment=comment_text)
        serializer = LongReviewCommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response({'error': 'Comment text is required'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def short_review_like(request, id):
    queryset = ShortReview.objects.filter(open=True).order_by('-created_at')
    review_id_list = list(queryset.values_list('id', flat=True))
    actual_id = review_id_list[int(id) - 1]
    review = get_object_or_404(ShortReview, id=actual_id, open=True)
    user = request.user
    if ShortReviewLike.objects.filter(review=review, user=user).exists():
        ShortReviewLike.objects.filter(review=review, user=user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        ShortReviewLike.objects.create(review=review, user=user)
        return Response(status=status.HTTP_201_CREATED)
