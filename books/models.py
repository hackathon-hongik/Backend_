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
    READING = '지금 읽고 있는 책', 'Reading'
    READ = '지금까지 읽은 책', 'Read'
    WISH = '찜해둔 책', 'Wish'
    

class MyBook(models.Model):
    member = models.ForeignKey(Member, on_delete= models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=128, choices=MyBookStatus.choices, default=MyBookStatus.WISH)
    totalpage = models.IntegerField()
    readpage = models.IntegerField()
    
    @property
    def readRate(self):
        return self.readpage / self.totalpage if self.readpage !=0 else 0
    

class Desk(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE)
    mybook = models.ForeignKey(MyBook, on_delete=models.CASCADE)
    readcount = models.IntegerField()
    readingcount = models.IntegerField()
    wishcount = models.IntegerField()
    
    
    
    