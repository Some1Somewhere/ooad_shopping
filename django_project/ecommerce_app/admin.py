from django.contrib import admin
from .models import Product, Order, CartItem

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display =['id', 'name', 'price']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'date', 'paid']


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'price', 'quantity', 'product']


admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(CartItem, OrderItemAdmin)