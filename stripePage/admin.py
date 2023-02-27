from django.contrib import admin
from .models import User, Item, Price

# Register your models here.

class PriceInlineAdmin(admin.TabularInline):
    model = Price
    extra = 0

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    inlines = [PriceInlineAdmin]

admin.site.register(User)
admin.site.register(Price)