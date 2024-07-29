from django.db import models
from members.models import Member 

class Book(models.Model):
    isbn = models.CharField(primary_key=True, max_length=300)
    title = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    date = models.DateTimeField(max_length=100)
    publisher = models.CharField(max_length=128)
    thumbnail = models.TextField()
    content = models.TextField()
    
    class Meta:
        db_table = 'books'
        
    def __str__(self):
        return self.title
    
class MyBookStatus(models.TextChoices):
    READING = 'reading'
    READ = 'read'
    WISH = 'wish'

class MyBook(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=128, choices=MyBookStatus.choices, default=MyBookStatus.WISH)
    
    class Meta:
        db_table = 'mybooks'

class Desk(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE)
    mybooks = models.ManyToManyField(MyBook, related_name='desks')
    read_count = models.PositiveIntegerField(default=0)
    reading_count = models.PositiveIntegerField(default=0)
    wish_count = models.PositiveIntegerField(default=0)
    
    def update_counts(self):
        self.read_count = self.mybooks.filter(status=MyBookStatus.READ).count()
        self.reading_count = self.mybooks.filter(status=MyBookStatus.READING).count()
        self.wish_count = self.mybooks.filter(status=MyBookStatus.WISH).count()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_counts()
        

    class Meta:
        db_table = 'desks'


    
    
    
    