from django.urls import path
from .views import LongReviewListView, LongReviewDetailView, ShortReviewListView, ShortReviewDetailView, long_review_like, long_review_comment, short_review_like

urlpatterns = [
    path('long-reviews/', LongReviewListView.as_view(), name='long_review_list'),
    path('long-reviews/<int:id>/', LongReviewDetailView.as_view(), name='long_review_detail'),
    path('short-reviews/', ShortReviewListView.as_view(), name='short_review_list'),
    path('short-reviews/<int:id>/', ShortReviewDetailView.as_view(), name='short_review_detail'),
    path('long-reviews/<int:id>/like/', long_review_like, name='long_review_like'),
    path('long-reviews/<int:id>/comment/', long_review_comment, name='long_review_comment'),
    path('short-reviews/<int:id>/like/', short_review_like, name='short_review_like'),

]
