from django.urls import path
from .views import long_review_list_create, long_review_detail, short_review_list_create, short_review_detail

urlpatterns = [
    path('desk/<int:memberID>/<int:myBookId>/note/long/', long_review_list_create, name='long_review_list_create'),
    path('desk/<int:memberID>/<int:myBookId>/note/long/<int:long_review_id>/', long_review_detail, name='long_review_detail'),
    path('desk/<int:memberID>/<int:myBookId>/note/short/', short_review_list_create, name='short_review_list_create'),
    path('desk/<int:memberID>/<int:myBookId>/note/short/<int:short_review_id>/', short_review_detail, name='short_review_detail'),
]