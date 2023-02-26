from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.decorators.http import require_POST, require_GET


from .models import Item
from .cart import Cart
from .forms import CartAddProductForm

# Create your views here.

class ItemListView(View):
    def get(self, request, *args, **kwargs):
        item_list = Item.objects.all()
        # items = Item.objects.all().order_by('-created_on')

        context = {
            'item_list': item_list
        }

        return render(request, 'stripePage/index.html', context)


class ItemDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        item = Item.objects.get(pk=pk)
        cart_product_form = CartAddProductForm()

        context = {
            'item': item,
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