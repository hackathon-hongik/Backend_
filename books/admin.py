from django.contrib import admin
from books.models import Book, MyBook, Desk
# Register your models here.

admin.site.register(Book)
admin.site.register(MyBook)
admin.site.register(Desk)
