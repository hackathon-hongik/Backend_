from django.db import models
from auths.models import CustomUser
from books.models import Book, MyBook, MyBookStatus

class MoodChoices(models.TextChoices):
    GOOD = 'good', 'Good'
    OKAY = 'okay', 'Okay'
    TIRED = 'tired', 'Tired'
    SAD = 'sad', 'Sad'
    WORRIED = 'worried', 'Worried'

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
    read_complete = models.BooleanField()
    mood = models.CharField(max_length=10, choices=MoodChoices.choices)
    question = models.CharField(max_length=10, choices=QuestionChoices.choices)
    answer = models.CharField(max_length=400)
    short_comment = models.CharField(max_length=300)
    open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'short_reviews'

    def __str__(self):
        return self.short_comment

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.read_complete:
            # 공백이 포함된 ISBN을 사용하여 Book 객체 생성 또는 조회
            book, created = Book.objects.get_or_create(
                isbn=self.book.isbn,
                defaults={
                    'title': self.book.title,
                    'author': self.book.author,
                    'date': self.book.date,
                    'publisher': self.book.publisher,
                    'thumbnail': self.book.thumbnail,
                    'content': self.book.content
                }
            )
            mybook, created = MyBook.objects.get_or_create(member=self.writer, book=book)
            if mybook.status != MyBookStatus.READ:
                mybook.status = MyBookStatus.READ
                mybook.save()

class LongReview(models.Model):
    writer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    start_page = models.PositiveIntegerField()
    end_page = models.PositiveIntegerField()
    read_complete = models.BooleanField()
    long_title = models.CharField(max_length=255)
    long_text = models.TextField()
    open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'long_reviews'

    def __str__(self):
        return self.long_title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.read_complete:
            # 공백이 포함된 ISBN을 사용하여 Book 객체 생성 또는 조회
            book, created = Book.objects.get_or_create(
                isbn=self.book.isbn,
                defaults={
                    'title': self.book.title,
                    'author': self.book.author,
                    'date': self.book.date,
                    'publisher': self.book.publisher,
                    'thumbnail': self.book.thumbnail,
                    'content': self.book.content
                }
            )
            mybook, created = MyBook.objects.get_or_create(member=self.writer, book=book)
            if mybook.status != MyBookStatus.READ:
                mybook.status = MyBookStatus.READ
                mybook.save()
