from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')


class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')


class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'description',
                    'category', 'genre_names')
    list_filter = ('category', 'year')
    search_fields = ('name', 'description')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title_id', 'text', 'pub_date', 'score')
    list_filter = ('pub_date',)
    search_fields = ('text',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'review_id', 'text', 'pub_date',)
    list_filter = ('pub_date',)
    search_fields = ('text',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
