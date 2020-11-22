from django.conf.urls import url

from .views import (
        RequestRefundView,
        OrderListView, 
        OrderDetailView
        )

urlpatterns = [
    url(r'^$', OrderListView.as_view(), name='list'),
    url(r'^(?P<order_id>[0-9A-Za-z]+)/$', OrderDetailView.as_view(), name='detail'),
    url('request-refund/', RequestRefundView.as_view(), name='request-refund'),
]