from django.urls import path
from books.views import add_book_to_status, desk_view, desk_group_view, mybook_detail, mainpage_view
from books.models import MyBookStatus

urlpatterns = [
    path('desk/books/wish/', add_book_to_status, {'status': MyBookStatus.WISH}, name='add_book_to_wish'),
    path('desk/books/reading/', add_book_to_status, {'status': MyBookStatus.READING}, name='add_book_to_reading'),
    path('desk/books/read/', add_book_to_status, {'status': MyBookStatus.READ}, name='add_book_to_read'),
    path('desk/books/', desk_view, name='desk_view'),
    path('desk/books/<str:isbn>/', mybook_detail, name='mybook_detail'),
    path('desk/books/group/<str:status>/', desk_group_view, name='desk_group_view'),
    path('mainpage/', mainpage_view, name='mainpage_view'),
]
