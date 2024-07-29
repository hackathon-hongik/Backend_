from django.shortcuts import render
from rest_framework import status as HTTPStatus
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from members.models import Member
from books.models import Book, MyBook, Desk, MyBookStatus
from books.serializers import MyBookSerializer, DeskSerializer

@api_view(['POST', 'GET'])
def add_book_to_status(request, memberId, status):
    member = get_object_or_404(Member, id=memberId)
    
    if request.method == 'POST':
        book_data = request.data.get('book')
        if not book_data:
            return Response({'error': 'Book data is required.'}, status=HTTPStatus.HTTP_400_BAD_REQUEST)    
        
        book, created = Book.objects.get_or_create(isbn=book_data['isbn'], defaults=book_data)   
        mybook, created = MyBook.objects.get_or_create(member=member, book=book)
        
        if not created and status == mybook.status:
            return Response({'error': 'This book is already in your list with the same status.'}, status=HTTPStatus.HTTP_409_CONFLICT)

        mybook.status = status
        mybook.save()
        
        return Response(MyBookSerializer(mybook).data, status=HTTPStatus.HTTP_200_OK)

    elif request.method == 'GET':
        mybooks = MyBook.objects.filter(member=member, status=status)
        serializer = MyBookSerializer(mybooks, many=True)
        return Response(serializer.data, status=HTTPStatus.HTTP_200_OK)

@api_view(['GET'])
def desk_view(request, memberId):
    member = get_object_or_404(Member, id=memberId)
    desk, created = Desk.objects.get_or_create(member=member)
    if created:
        desk.save()  # 새로 생성된 경우 저장하여 ID를 할당받음
    desk.update_counts()
    desk.save()  # 카운트 업데이트 후 저장
    serializer = DeskSerializer(desk)
    return Response(serializer.data, status=HTTPStatus.HTTP_200_OK)

@api_view(['GET'])
def mybook_detail(request, memberId, isbn):
    member = get_object_or_404(Member, id=memberId)
    book = get_object_or_404(Book, isbn=isbn)
    mybook = get_object_or_404(MyBook, member=member, book=book)
    serializer = MyBookSerializer(mybook)
    return Response(serializer.data, status=HTTPStatus.HTTP_200_OK)







        
    
