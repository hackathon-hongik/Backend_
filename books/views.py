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
        
        desk, desk_created = Desk.objects.get_or_create(member=member)
        
        if not created:
            if mybook.status == status:
                return Response({'error': 'This book is already in your list with the same status.'}, status=HTTPStatus.HTTP_409_CONFLICT)
            else:
                # Decrease the old status count
                desk, desk_created = Desk.objects.get_or_create(member=member)
                if mybook.status == MyBookStatus.WISH:
                    desk.wish_count -= 1
                elif mybook.status == MyBookStatus.READING:
                    desk.reading_count -= 1
                elif mybook.status == MyBookStatus.READ:
                    desk.read_count -= 1
               
        if status == MyBookStatus.WISH:
            desk.wish_count += 1
        elif status == MyBookStatus.READING:
            desk.reading_count += 1
        elif status == MyBookStatus.READ:
            desk.read_count += 1

        mybook.status = status
        mybook.save()
        
        # Desk 업데이트
        
        desk.mybooks.add(mybook)
        desk.save()
        
        return Response(MyBookSerializer(mybook).data, status=HTTPStatus.HTTP_200_OK)

    elif request.method == 'GET':
        sort_order = request.query_params.get('sort', 'newest')
        if sort_order == 'newest':
            mybooks = MyBook.objects.filter(member=member, status=status).order_by('-deskdate')
        elif sort_order == 'oldest':
            mybooks = MyBook.objects.filter(member=member, status=status).order_by('deskdate')
        else:
            mybooks = MyBook.objects.filter(member=member, status=status)
        
        serializer = MyBookSerializer(mybooks, many=True)
        return Response(serializer.data, status=HTTPStatus.HTTP_200_OK)

@api_view(['GET'])
def desk_view(request, memberId):
    member = get_object_or_404(Member, id=memberId)
    desk, created = Desk.objects.get_or_create(member=member)
    
    # Ensure desk object is saved to have an ID for many-to-many relation
    if created:
        desk.save()
    

    # Get all MyBooks associated with the member
    mybooks = MyBook.objects.filter(member=member)
    
    # Sorting functionality
    sort_order = request.query_params.get('sort', 'newest')
    if sort_order == 'newest':
        mybooks = mybooks.order_by('-deskdate')
    elif sort_order == 'oldest':
        mybooks = mybooks.order_by('deskdate')

    serializer = MyBookSerializer(mybooks, many=True)

    # Serialize desk data with mybooks
    response_data = {
        'member': member.id,
        'mybooks': serializer.data,
        'reading_count': desk.reading_count,
        'read_count': desk.read_count,
        'wish_count': desk.wish_count
    }
    
    return Response(response_data, status=HTTPStatus.HTTP_200_OK)

@api_view(['GET'])
def mybook_detail(request, memberId, isbn):
    member = get_object_or_404(Member, id=memberId)
    book = get_object_or_404(Book, isbn=isbn)
    mybook = get_object_or_404(MyBook, member=member, book=book)
    serializer = MyBookSerializer(mybook)
    return Response(serializer.data, status=HTTPStatus.HTTP_200_OK)







        
    
