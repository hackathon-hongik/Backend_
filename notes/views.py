from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import LongReview, ShortReview, Member, MyBook
from .serializers import LongReviewSerializer, ShortReviewSerializer

@api_view(['GET', 'POST'])
def long_review_list_create(request, memberID, myBookId):
    if request.method == 'GET':
        reviews = LongReview.objects.filter(member_id=memberID, my_book_id=myBookId)
        serializer = LongReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data.copy()
        data['member_id'] = memberID
        data['my_book_id'] = myBookId
        serializer = LongReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def long_review_detail(request, memberID, myBookId, long_review_id):
    review = get_object_or_404(LongReview, member_id=memberID, my_book_id=myBookId, long_review_id=long_review_id)

    if request.method == 'GET':
        serializer = LongReviewSerializer(review)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = request.data.copy()
        data['member_id'] = memberID
        data['my_book_id'] = myBookId
        serializer = LongReviewSerializer(review, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def short_review_list_create(request, memberID, myBookId):
    if request.method == 'GET':
        reviews = ShortReview.objects.filter(member_id=memberID, my_book_id=myBookId)
        serializer = ShortReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data.copy()
        data['member_id'] = memberID
        data['my_book_id'] = myBookId
        serializer = ShortReviewSerializer(data=data)
        if serializer.is_valid():
            review = serializer.save()
            # Determine the question based on the short_review_id (which is review.short_review_id)
            if review.short_review_id % 2 == 0:
                review.question = dict(ShortReview.QUESTION_TYPE_CHOICES)['2']
            else:
                review.question = dict(ShortReview.QUESTION_TYPE_CHOICES)['1']
            review.save()
            serializer = ShortReviewSerializer(review)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def short_review_detail(request, memberID, myBookId, short_review_id):
    review = get_object_or_404(ShortReview, member_id=memberID, my_book_id=myBookId, short_review_id=short_review_id)

    if request.method == 'GET':
        serializer = ShortReviewSerializer(review)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = request.data.copy()
        data['member_id'] = memberID
        data['my_book_id'] = myBookId
        serializer = ShortReviewSerializer(review, data=data)
        if serializer.is_valid():
            review = serializer.save()
            # Determine the question based on the short_review_id (which is review.short_review_id)
            if review.short_review_id % 2 == 0:
                review.question = dict(ShortReview.QUESTION_TYPE_CHOICES)['2']
            else:
                review.question = dict(ShortReview.QUESTION_TYPE_CHOICES)['1']
            review.save()
            serializer = ShortReviewSerializer(review)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
