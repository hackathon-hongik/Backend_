from rest_framework import serializers
from notes.models import LongReview, ShortReview
from books.models import Book
from .models import LongReviewLike, LongReviewComment, ShortReviewLike

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['isbn', 'title', 'author', 'date', 'publisher', 'thumbnail', 'content']

class LongReviewCommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.nickname')
    
    class Meta:
        model = LongReviewComment
        fields = ['id', 'user', 'comment', 'created_at']

class LongReviewSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    writer = serializers.ReadOnlyField(source='writer.nickname')
    long_note = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    comments = LongReviewCommentSerializer(many=True, read_only=True, source='longreviewcomment_set')
    is_liked = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()

    class Meta:
        model = LongReview
        fields = ['id', 'writer', 'book', 'long_note', 'like_count', 'comment_count', 'comments', 'is_liked']

    def get_long_note(self, obj):
        return {
            'review_id': obj.id,  # 리뷰 ID 추가
            'start_page': obj.start_page,
            'end_page': obj.end_page,
            'long_title': obj.long_title,
            'long_text': obj.long_text,
            'created_at': obj.created_at,
            'updated_at': obj.updated_at,
        }

    def get_like_count(self, obj):
        return LongReviewLike.objects.filter(review=obj).count()

    def get_comment_count(self, obj):
        return LongReviewComment.objects.filter(review=obj).count()

    def get_is_liked(self, obj):
        user = self.context.get('request').user
        return LongReviewLike.objects.filter(review=obj, user=user).exists()


    def get_id(self, obj):
        request = self.context.get('request')
        return request.id_list.index(obj.id) + 1 if hasattr(request, 'id_list') else obj.id

class ShortReviewSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    writer = serializers.ReadOnlyField(source='writer.nickname')
    short_note = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()

    class Meta:
        model = ShortReview
        fields = ['id', 'writer', 'book', 'short_note', 'like_count', 'is_liked']

    def get_short_note(self, obj):
        return {
            'review_id': obj.id,  # 리뷰 ID 추가
            'start_page': obj.start_page,
            'end_page': obj.end_page,
            'mood': obj.mood,
            'question': obj.question,
            'answer': obj.answer,
            'short_comment': obj.short_comment,
            'created_at': obj.created_at,
            'updated_at': obj.updated_at,
        }

    def get_like_count(self, obj):
        return ShortReviewLike.objects.filter(review=obj).count()

    def get_is_liked(self, obj):
        user = self.context.get('request').user
        return ShortReviewLike.objects.filter(review=obj, user=user).exists()


    def get_id(self, obj):
        request = self.context.get('request')
        return request.id_list.index(obj.id) + 1 if hasattr(request, 'id_list') else obj.id
