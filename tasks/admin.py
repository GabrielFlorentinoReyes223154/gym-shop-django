from django.contrib import admin
from .models import Product, Categoria, Carrito, ItemCarrito, Checkout,CheckoutItem

# Register your models here.

admin.site.register(Product)
admin.site.register(Categoria)
admin.site.register(Carrito)
admin.site.register(ItemCarrito)
admin.site.register(Checkout)
admin.site.register(CheckoutItem)