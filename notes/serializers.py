from rest_framework import serializers
from notes.models import LongReview, ShortReview, MoodChoices, QuestionChoices
from books.models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['isbn', 'title', 'author', 'date', 'publisher', 'thumbnail', 'content']

class LongReviewRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LongReview
        fields = ['start_page', 'end_page', 'read_complete', 'long_title', 'long_text', 'open']

class LongReviewSerializer(serializers.ModelSerializer):
    writer = serializers.CharField(source='writer.nickname')
    book = BookSerializer()
    long_note = serializers.SerializerMethodField()

    class Meta:
        model = LongReview
        fields = ['id', 'writer', 'created_at', 'book', 'long_note']

    def get_long_note(self, obj):
        return {
            'start_page': obj.start_page,
            'end_page': obj.end_page,
            'read_complete': obj.read_complete,
            'long_title': obj.long_title,
            'long_text': obj.long_text,
            'open': obj.open
        }

class ShortReviewRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortReview
        fields = ['start_page', 'end_page', 'read_complete', 'mood', 'question', 'answer', 'short_comment', 'long_title', 'long_text', 'open']

class ShortReviewSerializer(serializers.ModelSerializer):
    writer = serializers.CharField(source='writer.nickname')
    book = BookSerializer()
    short_note = serializers.SerializerMethodField()

    class Meta:
        model = ShortReview
        fields = ['id', 'writer', 'created_at', 'book', 'short_note']

    def get_short_note(self, obj):
        return {
            'start_page': obj.start_page,
            'end_page': obj.end_page,
            'read_complete': obj.read_complete,
            'mood': obj.get_mood_display(),
            'question': obj.get_question_display(),
            'answer': obj.answer,
            'short_comment': obj.short_comment,
            'long_title': obj.long_title,
            'long_text': obj.long_text,
            'open': obj.open
        }
