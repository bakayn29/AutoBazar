from django.db import models

from account.models import CustomUser


class Category(models.Model):
    slug = models.SlugField(primary_key=True, max_length=50)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=155)
    price = models.DecimalField(max_length=20)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    year = models.DecimalField(max_digits=10)
    color = models.CharField(max_length=55)
    engine = models.FloatField()
    box = models.CharField(max_length=20)
    drive_unit = models.CharField(max_length=20)
    steering_wheel = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description[:15] + '...'

    class Meta:
        ordering = ('-created', )


class ProductImage(models.Model):
    image = models.ImageField(upload_to='products', blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')


class Comment(models.Model):
    comment = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} -> {self.comment}"

    class Meta:
        ordering = ('created', )

    
