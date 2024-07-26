from django.db import models

# Create your models here.

class User(models.Model):
    nickname = models.CharField(max_length=30)
    
    class Meta:
        db_table = 'user'