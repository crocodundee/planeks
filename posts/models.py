from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.conf import settings

from django.utils import timezone
from django.urls import reverse

from slugify import Slugify, CYRILLIC
from ckeditor_uploader.fields import RichTextUploadingField
from posts.settings import *


def slugify(string):
    slug = Slugify(pretranslate=CYRILLIC,
                   to_lower=True,
                   max_length=24,
                   separator='-')
    return slug(string)


class PostQuerySet(models.QuerySet):
    def find(self, **kwargs):
        return self.filter(**kwargs)


class PostModelManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def approved_posts(self):
        return self.get_queryset().find(moderation_status='APPROVE')


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=256, verbose_name='Заголовок', unique=True)
    content = RichTextUploadingField(blank=True, null=True, verbose_name='Содержание')
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               verbose_name='Автор')
    created_at = models.DateField(auto_now=False,
                                  auto_now_add=False,
                                  default=timezone.now(),
                                  verbose_name='Дата публикации')
    slug = models.SlugField(null=True, blank=True)
    moderation_status = models.CharField(max_length=30,
                                         choices=ADMIN_CHOICES,
                                         default=ADMIN_CHOICES[0][1],
                                         verbose_name='Статус')

    objects = PostModelManager()

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = "Публикации"

    def __str__(self):
        return self.title

    def get_absolute_path(self, **kwargs):
        return reverse('post-view', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)


@receiver(pre_save, sender=Post)
def pre_save_post(sender, instance, *args, **kwargs):
    instance.slug = slugify(instance.title)


@receiver(post_save, sender=Post)
def set_moderation_status(sender, instance, created, *args, **kwargs):
    if created and not instance.author.user_group.moderation:
        instance.moderation_status = 'APPROVE'
        instance.save()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Публикация')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Комментатор')
    content = models.CharField(max_length=1024, blank=True, null=True, verbose_name="Ваш комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        db_table = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.post.title} - {self.author}'



