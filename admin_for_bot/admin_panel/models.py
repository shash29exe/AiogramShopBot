from django.db import models

class Users(models.Model):
    name = models.CharField(max_length=200)
    telegram = models.BigIntegerField(unique=True)
    phone = models.CharField(max_length=15, null=True, blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


    def __str__(self):
        return self.name

class Categories(models.Model):
    category_name = models.CharField(max_length=200, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.category_name

class Products(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='media/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='products')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.product_name