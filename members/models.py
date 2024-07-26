from django.db import models

# Create your models here.

class Member(models.Model):
    nickname = models.CharField(max_length=30)
