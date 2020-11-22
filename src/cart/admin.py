from django.contrib import admin


from .models import Cart, CartItem

class CartItemAdmin(admin.ModelAdmin):
    search_fields = ['cart__id']
    class Meta:
        model = CartItem

admin.site.register(Cart)
admin.site.register(CartItem,CartItemAdmin)
