from django.db import models
from auths.models import CustomUser
from notes.models import LongReview, ShortReview

class LongReviewLike(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    review = models.ForeignKey(LongReview, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class LongReviewComment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    review = models.ForeignKey(LongReview, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class ShortReviewLike(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    review = models.ForeignKey(ShortReview, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

