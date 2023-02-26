from django.urls import path
from .views import ItemListView, ItemDetailView, ShoppingCartView

from django.conf import settings
from django.conf.urls.static import static

app_name = 'stripePage'
urlpatterns = [
    path('', ItemListView.as_view(), name='item_list'),
    path('item/<int:pk>', ItemDetailView.as_view(), name='item_detail'),
    path('cart', ShoppingCartView.as_view(), name='cart'),
    path('cart/add/<int:item_pk>', ShoppingCartView.cart_add, name='cart_add'),
    path('cart/remove/<int:item_pk>', ShoppingCartView.cart_remove, name='cart_remove')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# path('item/<int:pk>', ItemDetailView.as_view(), name='item_detail')