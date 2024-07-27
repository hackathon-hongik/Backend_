from django.urls import path
from books.views import add_to_wish, add_to_reading, get_desk, get_books_by_status, delete_book

urlpatterns = [
    path('books/<int:memberId>/wish', add_to_wish, name='add_to_wish'),
    path('books/<int:memberId>/reading', add_to_reading, name='add_to_reading'),
    path('desk/<int:memberId>', get_desk, name='get_desk'),
    path('desk/<int:memberId>/<str:status>', get_books_by_status, name='get_books_by_status'),
    path('books/<int:memberId>/delete/<str:isbn>', delete_book, name='delete_book'),
]