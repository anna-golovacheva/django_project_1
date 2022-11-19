from django.db import models


class Locations(models.Model):
    name = models.CharField(max_length=300)
    lat = models.DecimalField(max_digits=8, decimal_places=6, null=True)
    lng = models.DecimalField(max_digits=8, decimal_places=6, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"

    def get_model_fields(cls):
        return cls._meta.fields


class Categories(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["id"]

    def get_model_fields(self):
        return self._meta.fields


class Users(models.Model):
    ROLES = [
        ('member', 'пользователь'),
        ('moderator', 'модератор'),
        ('admin', 'админ')
    ]

    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50, null=True, blank=True)
    role = models.CharField(max_length=50, choices=ROLES, default='member')
    age = models.IntegerField(null=True, blank=True)
    locations = models.ManyToManyField(Locations, null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ['username']

    def get_model_fields(self):
        return self._meta.fields


class Ads(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    author = models.ForeignKey(Users, on_delete=models.PROTECT)
    price = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    is_published = models.BooleanField(null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    category = models.ForeignKey(Categories, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    def get_model_fields(self):
        return self._meta.fields
