from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from members.models import Member
from books.models import Book, MyBook, Desk, MyBookStatus
from books.serializers import BookSerializer, MyBookSerializer, DeskSerializer

@api_view(['POST'])
def add_to_wish(request, memberId):
    member = get_object_or_404(Member, id=memberId)
    book_data = request.data.get('book')
    book, created = Book.objects.get_or_create(**book_data)
    
    mybook, created = MyBook.objects.get_or_create(member=member, book=book, defaults={'status': MyBookStatus.WISH})
    if not created:
        mybook.status = MyBookStatus.WISH
        mybook.save()

    Desk.objects.get_or_create(member=member)
    return Response(MyBookSerializer(mybook).data, status=status.HTTP_200_OK)

@api_view(['POST'])
def add_to_reading(request, memberId):
    member = get_object_or_404(Member, id=memberId)
    book_data = request.data.get('book')
    book, created = Book.objects.get_or_create(**book_data)
    
    # 중복 확인
    if MyBook.objects.filter(member=member, book=book, status=MyBookStatus.READING).exists():
        return Response({'error': 'This book is already in the reading list.'}, status=status.HTTP_409_CONFLICT)
    
    mybook, created = MyBook.objects.get_or_create(member=member, book=book, defaults={'status': MyBookStatus.READING})
    if not created:
        mybook.status = MyBookStatus.READING
        mybook.save()

    Desk.objects.get_or_create(member=member)
    return Response(MyBookSerializer(mybook).data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_desk(request, memberId):
    member = get_object_or_404(Member, id=memberId)
    desk, created = Desk.objects.get_or_create(member=member)
    
    order_by = request.query_params.get('order_by')
    if order_by == 'oldest':
        mybooks = MyBook.objects.filter(member=member).order_by('id')
    elif order_by == 'newest' or not order_by:
        mybooks = MyBook.objects.filter(member=member).order_by('-id')
    else:
        return Response({'error': 'Invalid order_by value'}, status=status.HTTP_400_BAD_REQUEST)

    desk_data = DeskSerializer(desk).data
    desk_data['mybooks'] = MyBookSerializer(mybooks, many=True).data
    
    return Response(desk_data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_books_by_status(request, memberId, status):
    member = get_object_or_404(Member, id=memberId)
    if status not in [choice[0] for choice in MyBookStatus.choices]:
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
    
    order_by = request.query_params.get('order_by')
    if order_by == 'oldest':
        mybooks = MyBook.objects.filter(member=member, status=status).order_by('id')
    elif order_by == 'newest' or not order_by:
        mybooks = MyBook.objects.filter(member=member, status=status).order_by('-id')
    else:
        return Response({'error': 'Invalid order_by value'}, status=status.HTTP_400_BAD_REQUEST)

    return Response(MyBookSerializer(mybooks, many=True).data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_book(request, memberId, isbn):
    member = get_object_or_404(Member, id=memberId)
    book = get_object_or_404(Book, isbn=isbn)
    mybook = MyBook.objects.filter(member=member, book=book).first()
    
    if mybook:
        mybook.delete()
        # Check if there are no more MyBook entries for this book
        if not MyBook.objects.filter(book=book).exists():
            book.delete()
        return Response({'message': 'Book deleted successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Book not found in user\'s collection'}, status=status.HTTP_404_NOT_FOUND)



        
    
