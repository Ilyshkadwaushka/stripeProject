from django.db import models
from django.template.defaultfilters import slugify


def get_image_filename(instance, filename):
    name = instance.name
    slug = slugify(name)
    return f"uploads/item_pictures/{slug}-{filename}"

class User(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return "Пользователь {0} - {1}".format(self.pk, self.name)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Item(models.Model):
    name = models.CharField(max_length=200, blank=True, null=False)
    description = models.TextField(max_length=500, blank=True, null=True)
    stripe_product_id = models.CharField(max_length=100, blank=False, null=True)
    thumbnail = models.ImageField(upload_to=get_image_filename, default='uploads/item_pictures/default.jpg', blank=True)
    quantity = models.IntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Товар {0} - {1}".format(self.pk, self.name)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

class Price(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    stripe_price_id = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.item.name} - {self.price}"