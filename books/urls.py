from django.urls import path
from books.views import add_to_wish, add_to_reading, get_mybook_by_isbn, get_books_by_status, get_desk

urlpatterns = [
    path('books/<int:memberId>/wish', add_to_wish, name='add_to_wish'),
    path('books/<int:memberId>/reading', add_to_reading, name='add_to_reading'),
    path('desk/<int:memberId>', get_desk, name='get_desk'),
    path('desk/<int:memberId>/<str:status>', get_books_by_status, name='get_books_by_status'),
   path('desk/<int:memberId>/<str:isbn>/', get_mybook_by_isbn, name='get_mybook_by_isbn'),
]