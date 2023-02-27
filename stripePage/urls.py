from django.urls import path
from .views import ItemListView, ItemDetailView, ShoppingCartView, CreateCheckoutSessionView, CancelView, SuccessView

from django.conf import settings
from django.conf.urls.static import static

app_name = 'stripePage'
urlpatterns = [
    path('', ItemListView.as_view(), name='item_list'),
    path('item/<int:pk>', ItemDetailView.as_view(), name='item_detail'),
    path('cart', ShoppingCartView.as_view(), name='cart'),
    path('cart/add/<int:item_pk>', ShoppingCartView.cart_add, name='cart_add'),
    path('cart/remove/<int:item_pk>', ShoppingCartView.cart_remove, name='cart_remove'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)