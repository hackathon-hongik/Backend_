from django.urls import path
from recommendations.views import worry_list, worry_book, worry_book_detail

urlpatterns = [
    path('recommendation/', worry_list, name='worry_list'),
    path('recommendation/<int:worryId>/book/', worry_book, name='worry_book'),
    path('recommendation/<int:worryId>/book/<int:id>/', worry_book_detail, name='worry_book_detail'),
]