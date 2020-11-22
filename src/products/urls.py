from django.conf.urls import url

from .views import (
        ProductListView,
        ProductListView2,
        ProductListView3,
        ProductPriceSort,

        
        # ProductDetailView,
        SingleView
        # ProductSlideView
        )

urlpatterns = [
    url(r'^parts/$', ProductListView, name='products'),
    url(r'^gears/$', ProductListView2, name='gears'),
    url(r'^bikes/$', ProductListView3, name='bikes'),
    url(r'^sort/$', ProductPriceSort, name='sort'),

    # url(r'^products/$', ProductListView1.as_view(), name='prod'),
    # url(r'^slider/$', ProductSlideView),

    url(r'^view/(?P<slug>[\w-]+)/$', SingleView, name='view')
]