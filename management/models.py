# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User



class MyUser(models.Model):
    user = models.OneToOneField(User)
    nickname = models.CharField(max_length=16)
    permission = models.IntegerField(default=1)

    def __unicode__(self):
        return self.user.username


class Comic(models.Model):
    name = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    publish_date = models.DateField()
    type = models.CharField(max_length=128)
    category = models.CharField(max_length=128)

    class META:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Img(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    img = models.ImageField(upload_to='image/%Y/%m/%d/')
    comic = models.ForeignKey(Comic)
    
    

    class META:
        ordering = ['name']

    def __unicode__(self):
        return self.name
    
class Carousel(models.Model):
    title = models.CharField(max_length=100, verbose_name=u'标题')
    summary = models.TextField(blank=True, null=True, verbose_name=u'摘要')
    img = models.CharField(max_length=200, verbose_name=u'轮播图片',
                           default='/static/img/carousel/default.jpg')
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)

    class Meta:
        verbose_name_plural = verbose_name = u'轮播'
        ordering = ['-create_time']