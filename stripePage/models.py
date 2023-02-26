from django.db import models
from django.utils import timezone

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return "Пользователь {0} - {1}".format(self.id, self.name)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Item(models.Model):
    name = models.CharField(max_length=100, blank=True, null=False)
    description = models.TextField(max_length=500, blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    picture = models.ImageField(upload_to='uploads/item_pictures', default='uploads/item_pictures/default.jpg', blank=False)

    def __str__(self):
        return "Товар {0} - {1} - {2}".format(self.id, self.name, self.price)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'