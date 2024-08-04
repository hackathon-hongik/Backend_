from django.shortcuts import render, get_object_or_404
from rest_framework import status as HTTPStatus
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from auths.models import CustomUser
from books.models import Book, MyBook, Desk, MyBookStatus
from books.serializers import MyBookSerializer, DeskSerializer

@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def add_book_to_status(request, status):
    member = request.user  # 인증된 사용자 가져오기
    
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
            elif mybook.status == MyBookStatus.READING and status == MyBookStatus.WISH:
                return Response({'error': 'Cannot add a reading book to wish list.'}, status=HTTPStatus.HTTP_400_BAD_REQUEST)
            else:
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
@permission_classes([IsAuthenticated])
def desk_view(request):
    member = request.user  # 인증된 사용자 가져오기
    desk, created = Desk.objects.get_or_create(member=member)
    
    desk.read_count = MyBook.objects.filter(member=member, status=MyBookStatus.READ).count()
    desk.reading_count = MyBook.objects.filter(member=member, status=MyBookStatus.READING).count()
    desk.wish_count = MyBook.objects.filter(member=member, status=MyBookStatus.WISH).count()
    desk.save()
    
    mybooks = MyBook.objects.filter(member=member)
    
    sort_order = request.query_params.get('sort', 'newest')
    if sort_order == 'newest':
        mybooks = mybooks.order_by('-deskdate')
    elif sort_order == 'oldest':
        mybooks = mybooks.order_by('deskdate')
    
    serializer = MyBookSerializer(mybooks, many=True)
    
    response_data = {
        'member': member.id,
        'mybooks': serializer.data,
        'reading_count': desk.reading_count,
        'read_count': desk.read_count,
        'wish_count': desk.wish_count
    }
    
    return Response(response_data, status=HTTPStatus.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def desk_group_view(request, status):
    member = request.user  # 인증된 사용자 가져오기
    desk, created = Desk.objects.get_or_create(member=member)
    
    if created:
        desk.save()
    
    mybooks = MyBook.objects.filter(member=member, status=status)
    
    sort_order = request.query_params.get('sort', 'newest')
    if sort_order == 'newest':
        mybooks = mybooks.order_by('-deskdate')
    elif sort_order == 'oldest':
        mybooks = mybooks.order_by('deskdate')
    
    serializer = MyBookSerializer(mybooks, many=True)
    
    response_data = {
        'member': member.id,
        'mybooks': serializer.data,
        'reading_count': desk.reading_count,
        'read_count': desk.read_count,
        'wish_count': desk.wish_count
    }
    
    return Response(response_data, status=HTTPStatus.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mybook_detail(request, isbn):
    member = request.user  # 인증된 사용자 가져오기
    book = get_object_or_404(Book, isbn=isbn)
    mybook = get_object_or_404(MyBook, member=member, book=book)
    serializer = MyBookSerializer(mybook)
    return Response(serializer.data, status=HTTPStatus.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mainpage_view(request):
    member = request.user  # 인증된 사용자 가져오기
    
    mybooks = MyBook.objects.filter(member=member, status=MyBookStatus.READING).order_by('-deskdate')[:2]
    reading_count = MyBook.objects.filter(member=member, status=MyBookStatus.READING).count()
    
    serializer = MyBookSerializer(mybooks, many=True)
    
    response_data = {
        'member': member.id,
        'recent_reading_books': serializer.data,
        'reading_count': reading_count
    }
    
    return Response(response_data, status=HTTPStatus.HTTP_200_OK)
