from django.contrib import admin
from .models import Post, Tag

# Register your models here.
# @admin.register(Author)
# class AuthorAdmin(admin.ModelAdmin):
#     list_display = ('name', 'email')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'slug')
    list_filter = ('published_date',)
    search_fields = ('title', 'content')
    # prepopulated_fields = {'slug':('title',)}
    ordering = ('-published_date',)