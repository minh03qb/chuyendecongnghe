from django.contrib import admin
from .models import Blog, Author, Entry, Comment

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('name', 'tagline')
    search_fields = ['name']

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ['name', 'email']

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('headline', 'blog', 'pub_date', 'status')
    list_filter = ('status', 'pub_date')
    search_fields = ['headline', 'body_text']
    date_hierarchy = 'pub_date'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('entry', 'author', 'created_date', 'approved')
    list_filter = ('approved', 'created_date')
    search_fields = ['text']
