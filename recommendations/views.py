from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from recommendations.models import Worry, WorryBook
from .serializers import WorryRequestSerializer, WorrySerializer, WorryBookRequestSerializer, WorryBookSerializer

@api_view(['GET', 'POST'])
def worry_list(request):
    if request.method == 'GET':
        worries = Worry.objects.all()
        serializer = WorrySerializer(worries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = WorryRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def worry_book(request, worryId):
    worry = get_object_or_404(Worry, id=worryId)
    if request.method == 'GET':
        worrybooks = WorryBook.objects.filter(worry=worry)
        serializer = WorryBookSerializer(worrybooks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        data = request.data.copy()
        data['worry'] = worry.id
        serializer = WorryBookRequestSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PATCH', 'DELETE'])
def worry_book_detail(request, worryId, id):
    worry = get_object_or_404(Worry, id=worryId)
    worrybook = get_object_or_404(WorryBook, worry=worry, id=id)
    
    if request.method == 'GET':
        serializer = WorryBookSerializer(worrybook)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PATCH':
        serializer = WorryBookRequestSerializer(worrybook, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        worrybook.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
  

# Create your views here.
