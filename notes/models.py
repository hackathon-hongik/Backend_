from django.db import models
from members.models import Member
from books.models import MyBook


# Create your models here.

class LongReview(models.Model):
    long_review_id = models.AutoField(primary_key=True)

    member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
    my_book_id = models.ForeignKey(MyBook, on_delete=models.CASCADE)

    start_page = models.IntegerField()
    end_page = models.IntegerField()
    read_complete = models.BooleanField(default=False)

    review_title = models.CharField(max_length=50)
    long_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    open = models.BooleanField(default=True)


class ShortReview(models.Model):
    MOOD_TYPE_CHOICES = {
        ('good', '좋아요'), #오른쪽에 있는 것이 화면에 보임
        ('okay', '괜찮아요'),
        ('tired', '피곤해요'),
        ('sad', '슬퍼요'),
        ('worried', '걱정돼요')
    }
    
    QUESTION_TYPE_CHOICES_1 = {
        ('1', '오늘 기분이 어때요?'),
        ('2', '오늘 날씨가 어때요?') #수정 필요 
    }
    QUESTION_TYPE_CHOICES_2 = {
        ('1', '오늘 기분이 어때요?'),
        ('2', '오늘 날씨가 어때요?') #수정 필요 
    }
    QUESTION_TYPE_CHOICES_3 = {
        ('1', '오늘 기분이 어때요?'),
        ('2', '오늘 날씨가 어때요?') #수정 필요 
    }
    QUESTION_TYPE_CHOICES_4 = {
        ('1', '오늘 기분이 어때요?'),
        ('2', '오늘 날씨가 어때요?') #수정 필요 
    }
    QUESTION_TYPE_CHOICES_5 = {
        ('1', '오늘 기분이 어때요?'),
        ('2', '오늘 날씨가 어때요?') #수정 필요 
    }

    short_review_id = models.AutoField(primary_key=True)

    member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
    my_book_id = models.ForeignKey(MyBook, on_delete=models.CASCADE)

    start_page = models.IntegerField()
    end_page = models.IntegerField()
    read_complete = models.BooleanField(default=False)

    mood = models.CharField(max_length=10, choices=MOOD_TYPE_CHOICES)
    question = models.CharField(max_length=400, choices=QUESTION_TYPE_CHOICES, default=True) #수정 필요 - 오류 pk받아라
    answer = models.CharField(max_length=300)

    short_comment = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    open = models.BooleanField(default=True) #로그인 되고 난 수정해야함

    

