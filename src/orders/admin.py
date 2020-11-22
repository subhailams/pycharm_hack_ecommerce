from django.contrib import admin

from .models import Order, Refund, OrderConfirmation

def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'
class OrderAdmin(admin.ModelAdmin):
    search_fields = [
        'billing_profile__email',
        'order_id'
    ]
    list_display = [
                        
                        'order_id',
                        'status',
                        'cash_on_delivery',
                        'being_delivered',
                        'refund_requested',
                        'refund_granted',
                        'timestamp'
                        
                        ]
    list_filter = ('status','billing_profile__email','being_delivered','refund_requested', 'refund_granted', 'cash_on_delivery')
    actions = [make_refund_accepted]
    class Meta:
        model = Order

admin.site.register(Order,OrderAdmin)
admin.site.register(Refund)
admin.site.register(OrderConfirmation)
