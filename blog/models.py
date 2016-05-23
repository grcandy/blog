# -*- coding:utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


from django.db import models
from django.db.models import signals
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.six import python_2_unicode_compatible



STATUS_CHOICES = (
    (1, '草稿'),
    (2, '发布')
)

def create_admin(*args, **kwargs):
    if User.objects.filter(username = "admin").exists():
        return
    User.objects.create_superuser("admin", "nobody@nowhere.com", "123456")

signals.post_migrate.connect(create_admin)


class PublishedManger(models.Manager):
    def get_queryset(self):
        return super(PublishedManger, self).get_queryset().filter(status=2)


@python_2_unicode_compatible
class Post(models.Model):
    title = models.CharField(max_length=250, verbose_name='标题')
    slug = models.SlugField(max_length=250, unique_for_date='publish', verbose_name='可跳转链接')
    author = models.ForeignKey(User, verbose_name='作者')
    body = models.TextField(verbose_name='内容', blank=True)
    publish = models.DateTimeField(default=timezone.now, verbose_name='发布时间')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    status = models.SmallIntegerField(verbose_name='状态', choices=STATUS_CHOICES, default=2)
    objects = models.Manager()
    published = PublishedManger()

    def __str__(self):
        return '博客：{}'.format(self.title)

    class Meta:
        ordering = ('-publish',)
        verbose_name = '博客'
        verbose_name_plural = verbose_name



