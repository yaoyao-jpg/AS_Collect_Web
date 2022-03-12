from django.db import models


# Create your models here.
class Lin_Fanfiction_And_Section_Data(models.Model):
    title = models.CharField(max_length=64)
    view = models.IntegerField()
    like = models.IntegerField()
    reply = models.IntegerField()
    score = models.FloatField()
    url = models.CharField(max_length=128)


class Lin_Video_Data(models.Model):
    title = models.CharField(max_length=256)
    view = models.IntegerField()
    like = models.IntegerField()
    coin = models.IntegerField()
    collect = models.IntegerField()
    score = models.FloatField()
    url = models.CharField(max_length=128)


class DouBan_Article(models.Model):
    title = models.CharField(max_length=256)
    author = models.CharField(max_length=128)
    like = models.IntegerField()
    collect = models.IntegerField()
    score = models.FloatField()
    url = models.CharField(max_length=128)


















