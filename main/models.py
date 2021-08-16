from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models

from account.models import CustomUser


class Category(models.Model):
    slug = models.SlugField(primary_key=True, max_length=100)
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=155)
    price = models.DecimalField(max_digits=20, decimal_places=3)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    year = models.CharField(max_length=5)
    color = models.CharField(max_length=55)
    engine = models.FloatField()
    box = models.CharField(max_length=20)
    drive_unit = models.CharField(max_length=20)
    steering_wheel = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created', )


class ProductImage(models.Model):
    image = models.ImageField(upload_to='products', blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')


class Comment(models.Model):
    comment = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} -> {self.comment}"

    class Meta:
        ordering = ('created', )


class RatingStar(models.Model):
    """Звезда рейтинга"""
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering = ["-value"]


class Rating(models.Model):
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='Звезда', related_name='ratings')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт', related_name='ratings')
    email = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='ratings')

    def __str__(self):
        return f"{self.star} - {self.product}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"









    
