from django.contrib import admin
from .models import Category, New, Author, NewCategory, Comment

admin.site.register(Category)
admin.site.register(New)
admin.site.register(Author)
admin.site.register(NewCategory)
admin.site.register(Comment)
