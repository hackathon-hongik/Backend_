# notes/models.py
from django.db import models
from auths.models import CustomUser
from books.models import Book

class LongReview(models.Model):
    writer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    start_page = models.PositiveIntegerField()
    end_page = models.PositiveIntegerField()
    read_complete = models.BooleanField(default=False)
    long_title = models.CharField(max_length=255)
    long_text = models.TextField()
    open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'long_reviews'
    
    def __str__(self):
        return self.long_title


from django.db import models
from auths.models import CustomUser
from books.models import Book

class MoodChoices(models.TextChoices):
    GOOD = 'good', '좋아요'
    OKAY = 'okay', '괜찮아요'
    TIRED = 'tired', '피곤해요'
    SAD = 'sad', '슬퍼요'
    WORRIED = 'worried', '걱정돼요'

class QuestionChoices(models.TextChoices):
    Q1 = 'Q1', '오늘 읽은 책이 나에게 어떤 도움이 될 수 있을까요?'
    Q2 = 'Q2', '책을 읽으면서 떠오른 나의 개인적인 경험이나 기억은 무엇인가요?'
    Q3 = 'Q3', '이 책을 읽으면서 가장 강렬하게 느꼈던 감정은 무엇인가요?'
    Q4 = 'Q4', '이 책이 나의 희망이나 두려움에 어떤 영향을 주었나요?'
    Q5 = 'Q5', '책의 내용을 통해 느낀 위로나 치유는 무엇인가요?'
    Q6 = 'Q6', '이 책이 나의 가치관이나 신념에 어떤 영향을 미쳤나요?'

class ShortReview(models.Model):
    writer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    start_page = models.PositiveIntegerField()
    end_page = models.PositiveIntegerField()
    read_complete = models.BooleanField(default=False)
    mood = models.CharField(max_length=10, choices=MoodChoices.choices)
    question = models.CharField(max_length=10, choices=QuestionChoices.choices)
    answer = models.CharField(max_length=200)
    short_comment = models.TextField()
    long_title = models.CharField(max_length=255)
    long_text = models.TextField()
    open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'short_reviews'
    
    def __str__(self):
        return self.long_title

# class MoodCount(models.Model):
#     member = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     book = models.ForeignKey(MyBook, on_delete=models.CASCADE)

#     good_count = models.PositiveIntegerField(default=0)
#     okay_count = models.PositiveIntegerField(default=0)
#     tired_count = models.PositiveIntegerField(default=0)
#     sad_count = models.PositiveIntegerField(default=0)
#     worried_count = models.PositiveIntegerField(default=0)
