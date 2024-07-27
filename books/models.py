from django.db import models
from members.models import Member 

# Create your models here.
class Book(models.Model):
    isbn = models.CharField(primary_key=True, max_length=300)
    title = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    thumbnail = models.CharField(max_length=128)
    content = models.TextField()
    
    class Meta:
        db_table = 'books'
        
class MyBookStatus(models.TextChoices):
    READING = 'reading'
    READ = 'read'
    WISH = 'wish'
    

class MyBook(models.Model):
    member = models.ForeignKey(Member, on_delete= models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=128, choices=MyBookStatus.choices, default=MyBookStatus.WISH)

    

class Desk(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE)
    mybooks = models.ManyToManyField(MyBook)
    
    @property
    def read_count(self):
        return self.mybooks.filter(status=MyBookStatus.READ).count()
    
    @property
    def reading_count(self):
        return self.mybooks.filter(status=MyBookStatus.READING).count()
    
    @property
    def wish_count(self):
        return self.mybooks.filter(status=MyBookStatus.WISH).count()

    class Meta:
        db_table = 'desks'
    
    
    
    
    