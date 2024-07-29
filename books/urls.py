from django.urls import path
from books.views import add_book_to_status, desk_view, mybook_detail
from books.models import MyBookStatus

urlpatterns = [
    path('desk/<int:memberId>/books/wish/', add_book_to_status, {'status': MyBookStatus.WISH}, name='add_book_to_wish'),
    path('desk/<int:memberId>/books/reading/', add_book_to_status, {'status': MyBookStatus.READING}, name='add_book_to_reading'),
    path('desk/<int:memberId>/books/', desk_view, name='desk_view'),
    path('desk/<int:memberId>/books/<str:isbn>/', mybook_detail, name='mybook_detail'),
]