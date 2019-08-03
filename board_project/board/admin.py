from django.contrib import admin
from .models import Category, Document, Comment
# Register your models here.

class CategoryOption(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    prepopulated_fields = {'slug':('name',)}

class CommentInline(admin.TabularInline):
    model = Comment

class DocumentOption(admin.ModelAdmin):
    list_display = ['id', 'author', 'title', 'text', 'slug', 'created', 'updated']
    prepopulated_fields = {'slug':('title',)}
    inlines = [CommentInline]

admin.site.register(Category, CategoryOption)

admin.site.register(Document, DocumentOption)

admin.site.register(Comment)