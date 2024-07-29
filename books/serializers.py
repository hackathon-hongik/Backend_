from rest_framework import serializers
from books.models import Book, MyBook, Desk

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['isbn', 'title', 'author', 'date', 'publisher', 'thumbnail', 'content']

class MyBookSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    
    class Meta:
        model = MyBook
        fields = ['member', 'book', 'status']
        
    def create(self, validated_data):
        book_data = validated_data.pop('book')
        book, created = Book.objects.get_or_create(isbn=book_data['isbn'], defaults=book_data)
        mybook = MyBook.objects.create(book=book, **validated_data)
        return mybook


class DeskSerializer(serializers.ModelSerializer):
    mybooks = MyBookSerializer(many=True, read_only=True)

    
    class Meta:
        model = Desk
        fields = ['mybooks', 'reading_count', 'read_count', 'wish_count']


    
    
    
    
    
    
    
    
    