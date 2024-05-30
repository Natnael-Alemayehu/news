from django.contrib import admin
from articles.models import Article


# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "body",
        "author",
    ]


admin.site.register(Article, ArticleAdmin)
