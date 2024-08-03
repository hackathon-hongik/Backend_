from rest_framework import status as HTTPStatus
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from notes.models import LongReview, ShortReview
from notes.serializers import LongReviewRequestSerializer, LongReviewSerializer, ShortReviewRequestSerializer, ShortReviewSerializer
from books.models import Book, MyBook, MyBookStatus
import urllib.parse

def decode_isbn(isbn):
    return urllib.parse.unquote(isbn)

@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def long_review_list(request, isbn):
    member = request.user  # 인증된 사용자 가져오기
    isbn_decoded = decode_isbn(isbn)  # ISBN에서 URL 인코딩 제거
    
    # Book 객체가 데이터베이스에 존재하는지 확인
    book = get_object_or_404(Book, isbn=isbn_decoded)

    if request.method == 'POST':
        data = request.data
        serializer = LongReviewRequestSerializer(data=data)
        if serializer.is_valid():
            long_review = serializer.save(writer=member, book=book)
            response_serializer = LongReviewSerializer(long_review)
            response_data = response_serializer.data
            response_data['book']['isbn'] = isbn  # 디코딩된 ISBN 반환
            return Response(response_data, status=HTTPStatus.HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTPStatus.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        long_reviews = LongReview.objects.filter(book=book, writer=member)
        serializer = LongReviewSerializer(long_reviews, many=True)
        response_data = serializer.data
        for item in response_data:
            item['book']['isbn'] = isbn  # 디코딩된 ISBN 반환
        return Response(response_data, status=HTTPStatus.HTTP_200_OK)

@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def long_review_detail(request, isbn, id):
    member = request.user  # 인증된 사용자 가져오기
    isbn_decoded = decode_isbn(isbn)  # ISBN에서 URL 인코딩 제거
    book = get_object_or_404(Book, isbn=isbn_decoded)
    long_review = get_object_or_404(LongReview, book=book, writer=member, id=id)

    if request.method == 'GET':
        serializer = LongReviewSerializer(long_review)
        response_data = serializer.data
        response_data['book']['isbn'] = isbn  # 디코딩된 ISBN 반환
        return Response(response_data, status=HTTPStatus.HTTP_200_OK)

    elif request.method == 'PATCH':
        serializer = LongReviewRequestSerializer(long_review, data=request.data, partial=True)
        if serializer.is_valid():
            long_review = serializer.save()
            response_serializer = LongReviewSerializer(long_review)
            response_data = response_serializer.data
            response_data['book']['isbn'] = isbn  # 디코딩된 ISBN 반환
            return Response(response_data, status=HTTPStatus.HTTP_200_OK)
        return Response(serializer.errors, status=HTTPStatus.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        long_review.delete()
        return Response(status=HTTPStatus.HTTP_204_NO_CONTENT)

@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def short_review_list(request, isbn):
    member = request.user  # 인증된 사용자 가져오기
    isbn_decoded = decode_isbn(isbn)  # ISBN에서 URL 인코딩 제거
    
    # Book 객체가 데이터베이스에 존재하는지 확인
    book = get_object_or_404(Book, isbn=isbn_decoded)

    if request.method == 'POST':
        data = request.data
        serializer = ShortReviewRequestSerializer(data=data)
        if serializer.is_valid():
            short_review = serializer.save(writer=member, book=book)
            response_serializer = ShortReviewSerializer(short_review)
            response_data = response_serializer.data
            response_data['book']['isbn'] = isbn  # 디코딩된 ISBN 반환
            return Response(response_data, status=HTTPStatus.HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTPStatus.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        short_reviews = ShortReview.objects.filter(book=book, writer=member)
        serializer = ShortReviewSerializer(short_reviews, many=True)
        response_data = serializer.data
        for item in response_data:
            item['book']['isbn'] = isbn  # 디코딩된 ISBN 반환
        return Response(response_data, status=HTTPStatus.HTTP_200_OK)

@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def short_review_detail(request, isbn, id):
    member = request.user  # 인증된 사용자 가져오기
    isbn_decoded = decode_isbn(isbn)  # ISBN에서 URL 인코딩 제거
    book = get_object_or_404(Book, isbn=isbn_decoded)
    short_review = get_object_or_404(ShortReview, book=book, writer=member, id=id)

    if request.method == 'GET':
        serializer = ShortReviewSerializer(short_review)
        response_data = serializer.data
        response_data['book']['isbn'] = isbn  # 디코딩된 ISBN 반환
        return Response(response_data, status=HTTPStatus.HTTP_200_OK)

    elif request.method == 'PATCH':
        serializer = ShortReviewRequestSerializer(short_review, data=request.data, partial=True)
        if serializer.is_valid():
            short_review = serializer.save()
            response_serializer = ShortReviewSerializer(short_review)
            response_data = response_serializer.data
            response_data['book']['isbn'] = isbn  # 디코딩된 ISBN 반환
            return Response(response_data, status=HTTPStatus.HTTP_200_OK)
        return Response(serializer.errors, status=HTTPStatus.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        short_review.delete()
        return Response(status=HTTPStatus.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def short_review_mood_list(request, isbn):
    member = request.user  # 인증된 사용자 가져오기
    isbn_decoded = decode_isbn(isbn)  # ISBN에서 URL 인코딩 제거
    book = get_object_or_404(Book, isbn=isbn_decoded)

    short_reviews = ShortReview.objects.filter(book=book)
    serializer = ShortReviewSerializer(short_reviews, many=True)
    
    response_data = {
        "short_notes": serializer.data,
        "good_count": short_reviews.filter(mood='good').count(),
        "okay_count": short_reviews.filter(mood='okay').count(),
        "tired_count": short_reviews.filter(mood='tired').count(),
        "sad_count": short_reviews.filter(mood='sad').count(),
        "worried_count": short_reviews.filter(mood='worried').count(),
    }
    
    for item in response_data["short_notes"]:
        item['book']['isbn'] = isbn  # 디코딩된 ISBN 반환
    
    return Response(response_data, status=HTTPStatus.HTTP_200_OK)
