from django.urls import path
from notes.views import long_review_list, long_review_detail, short_review_list, short_review_detail, short_review_mood_list

urlpatterns = [
    path('desk/books/<str:isbn>/note/long', long_review_list, name='long_review_create_or_get'),
    path('desk/books/<str:isbn>/note/short', short_review_list, name='short_review_create_or_get'),
    path('desk/books/<str:isbn>/note/long/<int:id>', long_review_detail, name='long_review_modify_or_delete'),
    path('desk/books/<str:isbn>/note/short/<int:id>', short_review_detail, name='short_review_modify_or_delete'),
    path('desk/books/<str:isbn>/note/mood', short_review_mood_list, name='short_review_mood_list'),
]
