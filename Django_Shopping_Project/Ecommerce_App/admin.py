from django.contrib import admin
from .models import Customer, Product, Cart, OrderPlaced
from django.utils.html import format_html
from django.urls import reverse


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'locality', 'city', 'zipcode', 'state')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'selling_price', 'discounted_price', 'description', 'brand', 'category', 'profile_image')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity')


@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'customer_info', 'product_info', 'product', 'quantity', 'ordered_date', 'status')
    list_filter = ('status', 'ordered_date')
    search_fields = ('user__username', 'customer__name', 'product__title')
    list_editable = ('status',)
    ordering = ('-ordered_date',)
    
    
    def customer_info(self, obj):
        link = reverse("admin:Ecommerce_App_customer_change", args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>', link, obj.customer.name)
    
    customer_info.short_description = "Customer"

    
    def product_info(self, obj):
        link = reverse("admin:Ecommerce_App_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)
    
    product_info.short_description = "Product"