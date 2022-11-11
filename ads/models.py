from django.db import models


class Ads(models.Model):
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    price = models.IntegerField()
    description = models.CharField(max_length=500)
    is_published = models.BooleanField()

    def __str__(self):
        return self.name


class Categories(models.Model):
    name = models.CharField(max_length=100)
