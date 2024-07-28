from rest_framework import serializers
from books.models import Book, MyBook, Desk

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['isbn', 'title', 'author', 'thumbnail', 'content']

class MyBookRequestSerializer(serializers.ModelSerializer):
    memberId = serializers.IntegerField(source='member.id')
    book = BookSerializer()
    
    class Meta:
        model = MyBook
        fields = ['memberId', 'book']

class MyBookSerializer(serializers.ModelSerializer):
    memberId = serializers.IntegerField(source='member.id')
    book = BookSerializer()
    
    class Meta:
        model = MyBook
        fields = ['memberId', 'id', 'book', 'status']

class DeskSerializer(serializers.ModelSerializer):
    mybooks = MyBookSerializer(many=True, read_only=True)
    reading_count = serializers.SerializerMethodField()
    read_count = serializers.SerializerMethodField()
    wish_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Desk
        fields = ['mybooks', 'reading_count', 'read_count', 'wish_count']

    def get_reading_count(self, obj):
        return obj.reading_count

    def get_read_count(self, obj):
        return obj.read_count

    def get_wish_count(self, obj):
        return obj.wish_count


    
    
    
    
    
    
    
    
    