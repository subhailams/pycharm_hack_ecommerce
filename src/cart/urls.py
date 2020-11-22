from django.conf.urls import url

from .views import (
        cart_home, 
        cart_update,
        cart_login,
        checkout_home,
        checkout_done_view,
        cart_detail_api_view,
        )
# app_name='cart'

urlpatterns = [
    url(r'^$', cart_home, name='cart'),
    url(r'^update/$', cart_update, name='update'),
    url(r'^login/',cart_login ,name='login'),
    url(r'^checkout/$', checkout_home, name='checkout'),
    url(r'^checkout/success$', checkout_done_view, name='success'),
    url(r'^cart/api/cart/$', cart_detail_api_view, name='api-cart'),
]