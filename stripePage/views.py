import stripe

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.decorators.http import require_POST
from django.conf import settings
from django.views.generic import TemplateView

from .models import Item, Price
from .cart import Cart
from .forms import CartAddProductForm

stripe.api_key = settings.STRIPE_SECRET_KEY

class ItemListView(View):

    def get(self, request, *args, **kwargs):
        item_list = Item.objects.all()

        context = {
            'item_list': item_list
        }

        return render(request, 'stripePage/index.html', context)


class ItemDetailView(View):

    def get(self, request, pk, *args, **kwargs):
        item = Item.objects.get(pk=pk)
        price = str(Price.objects.select_related('item').filter(pk=pk).get().price)
        cart_product_form = CartAddProductForm()

        context = {
            'item': item,
            'price': price,
            'cart_product_form': cart_product_form
        }

        return render(request, 'stripePage/itemView.html', context)



class ShoppingCartView(View):

    def get(self, request, *args, **kwargs):

        cart = Cart(request)

        for item in cart:
            item['override_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                    'update': True})

        context = {
            'cart': cart
        }

        return render(request, 'stripePage/shoppingCart.html', context)

    @require_POST
    @staticmethod
    def cart_add(request, item_pk, *args, **kwargs):
        cart = Cart(request)
        item = get_object_or_404(Item, id = item_pk)
        form = CartAddProductForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            cart.add(item=item,
                     quantity=cd['quantity'],
                     override_quantity=cd['update'])

        return redirect('stripePage:cart')

    @staticmethod
    def cart_remove(request, item_pk, *args, **kwargs):
        cart = Cart(request)
        item = get_object_or_404(Item, id=item_pk)
        cart.remove(item)

        return redirect('stripePage:cart')

class CreateCheckoutSessionView(View):

    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        domain = "https://yourdomain.com"

        if settings.DEBUG:
            domain = "http://127.0.0.1:8000"

        line_items = []
        for item in cart:
            line_items.append({'price': Price.objects.select_related('item').filter(pk=item['item'].pk).get().stripe_price_id, 'quantity': item['quantity']})

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=domain + '/success/',
            cancel_url=domain + '/cancel/',
        )
        return redirect(checkout_session.url)

class SuccessView(TemplateView):
    template_name = "stripePage/success.html"

    def setup(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs

        cart = Cart(request)
        cart.clear()

class CancelView(TemplateView):
    template_name = "stripePage/cancel.html"