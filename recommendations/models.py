from django.db import models
from books.models import Book


# Create your models here.
class Worry(models.Model):
    worry = models.CharField(max_length = 128)
    
    def __str__(self):
        return self.worry

class WorryBook(models.Model):
    worry = models.ForeignKey(Worry, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.book)
    
    
