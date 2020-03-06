from django.contrib import admin
from posts.models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'moderation_status')
    list_editable = ('moderation_status',)
    list_filter = ('moderation_status', 'created_at', 'author', )
    actions = ('approve_posts', 'decline_posts',)

    def approve_posts(self, request, queryset):
        for post in queryset:
            post.moderation_status = 'APPROVE'
            post.save()
    approve_posts.short_description = 'Опубликовать выбранные'

    def decline_posts(self, request, queryset):
        for post in queryset:
            post.moderation_status = 'DECLINE'
            post.save()
    decline_posts.short_description = 'Вернуть в неопубликованные'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at',)
    list_filter = ('post', 'author',)


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)

