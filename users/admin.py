from django.contrib import admin
from django.contrib.auth.models import Group
from users.models import User
from users.groups import UserGroup


class UserAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name', 'email', 'password', 'user_group', ]
    list_display = ['email', 'full_name', 'user_group']
    list_editable = ['user_group', ]
    list_filter = ('user_group', 'date_joined')
    ordering = ('date_joined',)
    actions = ('add_as_admin', 'add_as_editor', 'add_as_user',)

    def add_as_admin(self, request, queryset):
        admins = UserGroup.objects.get(id=1)
        for user in queryset:
            user.user_group = admins
            user.save()
    add_as_admin.short_description = "Добавить в группу 'Администраторы'"

    def add_as_editor(self, request, queryset):
        editors = UserGroup.objects.get(id=2)
        for user in queryset:
            user.user_group = editors
            user.save()
    add_as_editor.short_description = "Добавить в группу 'Редакторы'"

    def add_as_user(self, request, queryset):
        users = UserGroup.objects.get(id=3)
        for user in queryset:
            user.user_group = users
            user.save()
    add_as_user.short_description = "Добавить в группу 'Пользователи'"


class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'moderation')
    list_editable = ('moderation',)
    ordering = ['id', ]


admin.site.register(User, UserAdmin)
admin.site.register(UserGroup, GroupAdmin)
admin.site.unregister(Group)


