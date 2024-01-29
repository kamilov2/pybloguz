from typing import Any
from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest

from blog.models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    prepopulated_fields = {'slug':('title',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    prepopulated_fields = {'slug':('title',)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "is_top", "is_slider")
    search_fields = ["title"]
    list_filter = ("is_top", "is_slider", "is_published", "published_date")
    prepopulated_fields = {'slug':('title',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("full_name", "published_date")
    
@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ("title", "link")
    
@admin.register(InstagramPost)
class InstagramAdmin(admin.ModelAdmin):
    list_display = ("id", "link")
