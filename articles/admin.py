from django.contrib import admin
from articles.models import Article, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = [
        "comment",
        "article",
        "author",
    ]


class ArticleAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]
    list_display = [
        "title",
        "body",
        "author",
    ]


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
