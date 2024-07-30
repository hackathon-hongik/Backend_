from django.contrib import admin

# Register your models here.
from recommendations.models import Worry, WorryBook
# Register your models here.

admin.site.register(WorryBook)
admin.site.register(Worry)
