from django.conf import settings
from .models import Item
from decimal import Decimal

class Cart:
    def __init__(self, request):
        """ Initializing Cart """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def add(self, item: Item, quantity=1, override_quantity = False):
        item_pk = str(item.pk)
        if item_pk not in self.cart:
            self.cart[item_pk] = {'quantity': 0, 'price': str(item.price)}

        if override_quantity:
            self.cart[item_pk]['quantity'] = quantity
        else:
            self.cart[item_pk]['quantity'] += quantity

        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, item: Item):
        item_pk = str(item.pk)
        if item_pk in self.cart:
            del self.cart[item_pk]
            self.save()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def __iter__(self):
        item_ids = self.cart.keys()
        items = Item.objects.filter(id__in = item_ids)

        cart = self.cart.copy()
        for item in items:
            cart[str(item.pk)]['item'] = item

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
