from django.urls import path
from .views import member_list, member_detail

urlpatterns = [
    path('member/', member_list),
    path('member/<int:id>/', member_detail)
]
