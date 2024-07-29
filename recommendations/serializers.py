from rest_framework import serializers
from recommendations.models import Worry, WorryBook
from books.models import Book
from books.serializers import BookSerializer

class WorryRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worry
        fields = ['worry']

class WorrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Worry
        fields = ['id', 'worry']

class WorryBookRequestSerializer(serializers.ModelSerializer):
    worryId = serializers.IntegerField(source='worry.id')
    book = BookSerializer()

    class Meta:
        model = WorryBook
        fields = ['worryId', 'book']

    def create(self, validated_data):
        book_data = validated_data.pop('book')
        worry = validated_data.pop('worry')
        
        # Create or get the book instance
        book, created = Book.objects.get_or_create(**book_data)
        
        # Create the WorryBook instance
        worrybook = WorryBook.objects.create(worry=worry, book=book)
        
        return worrybook

class WorryBookSerializer(serializers.ModelSerializer):
    worryId = serializers.IntegerField(source='worry.id')
    book = BookSerializer()

    class Meta:
        model = WorryBook
        fields = ['worryId', 'id', 'book']

        

    