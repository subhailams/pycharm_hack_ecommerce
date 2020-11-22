from django.contrib import admin

from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'slug', 'category', 'price']
    list_filter = ('category','price')
    class Meta:
        model = Product


admin.site.register(Product,ProductAdmin)