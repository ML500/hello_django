from django.contrib import admin
from webapp.models import Article, Comment, Tag, ArticleLike, CommentLike


class ArticleAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags',)
    readonly_fields = ('like_count',)


class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ('like_count',)


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Tag)
admin.site.register(ArticleLike)
admin.site.register(CommentLike)
