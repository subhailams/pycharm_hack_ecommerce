from django.conf.urls import url
from .views import (
    # initiate_payment,
    # callback,
    razor_pay,
    payment_status,
    cash_on_delivery
    )

urlpatterns = [
    #    url(r'^pay/$', initiate_payment, name='payment'),
    #    url(r'^callback/$', callback, name='callback'),
       url(r'^razor/', razor_pay, name='razor'),
       url(r'^payment_status/$', payment_status, name='payment_status'),
       url(r'^order_confirm/$',cash_on_delivery, name='cash_on_delivery')
]