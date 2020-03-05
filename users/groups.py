from django.db import models


class UserGroup(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name='Группа')
    moderation = models.BooleanField(default=True, verbose_name='Премодерация публикаций')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return f'{self.name}'
