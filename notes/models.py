from django.db import models
from auths.models import CustomUser
from books.models import Book, MyBook, MyBookStatus, Desk

class MoodChoices(models.TextChoices):
    GOOD = 'good', 'Good'
    OKAY = 'okay', 'Okay'
    TIRED = 'tired', 'Tired'
    SAD = 'sad', 'Sad'
    WORRIED = 'worried', 'Worried'

class QuestionChoices(models.TextChoices):
    Q1 = 'Q1', '인간 관계 - 중요한 대화를 해야 할 때, 갈등을 피하기 위해 어떤 준비를 하나요?'
    Q2 = 'Q2', '인간 관계 - 인간 관계에서 자신의 감정을 효과적으로 표현하는 방법은 무엇인가요?'
    Q3 = 'Q3', '진로 - 책의 주요 메시지나 교훈이 내 현재 진로 고민에 어떤 통찰을 제공했나요?'
    Q4 = 'Q4', '진로 - 책을 읽고 나서 내 진로에 대한 새로운 아이디어나 방향성이 생겼다면, 그것을 구체적으로 어떻게 실행할 수 있을까요?'
    Q5 = 'Q5', '경제 - 책을 통해 알게 된 투자 리스크 관리 방법 중 나에게 적합한 것은 무엇이며, 그것을 어떻게 실행할 수 있을까요?'
    Q6 = 'Q6', '경제 - 책에서 소개된 성공적인 재정 관리 사례를 내 삶에 적용한다면, 어떤 변화가 필요할까요?'
    Q7 = 'Q7', '건강 - 이 책에서 배운 중요한 건강 관리 원칙은 무엇이며, 그것을 어떻게 내 생활에 적용할 수 있을까요?'
    Q8 = 'Q8', '건강 - 책에서 소개된 성공적인 건강 관리 사례를 내 삶에 적용한다면, 어떤 변화가 필요할까요?'
    Q9 = 'Q9', '직장 생활 - 내가 직장에서 버겁게 느끼는 부분은 무엇이며, 책에서 제안한 해결책 중 어떤 것을 시도해볼 수 있을까요?'
    Q10 = 'Q10', '직장 생활 - 책을 읽고 난 후 나의 직장 업무 방식을 재구성해야 한다면, 어떤 변화가 필요하다고 생각하나요?'
    

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
            desk, created = Desk.objects.get_or_create(member=self.writer)
            
            # 기존 상태에 따른 카운트 감소
            if mybook.status == MyBookStatus.READING:
                desk.reading_count -= 1
            elif mybook.status == MyBookStatus.WISH:
                desk.wish_count -= 1
            
            # 새로운 상태에 따른 카운트 증가
            if mybook.status != MyBookStatus.READ:
                mybook.status = MyBookStatus.READ
                mybook.save()
                desk.read_count += 1
                desk.save()

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
            desk, created = Desk.objects.get_or_create(member=self.writer)
            
            # 기존 상태에 따른 카운트 감소
            if mybook.status == MyBookStatus.READING:
                desk.reading_count -= 1
            elif mybook.status == MyBookStatus.WISH:
                desk.wish_count -= 1
            
            # 새로운 상태에 따른 카운트 증가
            if mybook.status != MyBookStatus.READ:
                mybook.status = MyBookStatus.READ
                mybook.save()
                desk.read_count += 1
                desk.save()
