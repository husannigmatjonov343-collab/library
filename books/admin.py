from django.contrib import admin
from .models import Category, Article, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'category', 'created_date', 'comments_count']
    list_filter = ['category', 'created_date']
    search_fields = ['title', 'content']
    raw_id_fields = ['author']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'article', 'created_date']
    list_filter = ['created_date']