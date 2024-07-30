from rest_framework import serializers
from .models import LongReview, ShortReview

class LongReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = LongReview
        fields = [ 'long_review_id', 'member_id', 'my_book_id', 'start_page', 'end_page', 'read_complete', 'review_title', 'long_text', 'created_at', 'open']

class ShortReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortReview
        fields = [ 'short_review_id', 'member_id', 'my_book_id', 'start_page', 'end_page', 'read_complete', 'mood', 'question', 'answer', 'short_comment', 'created_at', 'open' ]