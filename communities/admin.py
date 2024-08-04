from django.contrib import admin
from communities.models import ShortReviewLike,  LongReviewComment, LongReviewLike
# Register your models here.

admin.site.register(ShortReviewLike)
admin.site.register(LongReviewComment)
admin.site.register(LongReviewLike)