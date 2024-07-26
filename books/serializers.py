from rest_framework import serializers

from members.models import Member
from books.models import Book, MyBook, MyBookStatus, Desk

class BookRequestSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Book
        fields = '__all__'
        
class MyBookSerializer(serializers.Serializer):
    mybookId = serializers.CharField(source = 'id')
    myBookTitle = serializers.CharField(source = 'title')
    myBookAuthor = serializers.CharField(source = 'author')
    mybookThumbnail = serializers.CharField(source = 'thumbnail')
    myBookStatus = serializers.CharField(source = 'status')
    
class DeskSerializer(serializers.Serializer):
    memberId = serializers.IntegerField(source='member.id')
    books = MyBookSerializer(many=True)
    readCount = serializers.IntegerField(source = 'read_count')
    readingCount = serializers.IntegerField(souce = 'reading_count')
    wishCount = serializers.IntegerField(source = 'wish_count')
    
    
    
    
    
    
    