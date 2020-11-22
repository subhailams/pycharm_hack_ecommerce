"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

from django.conf.urls import url,include
from django.contrib import admin
from .views import home_page,access,logout_page,contact_page,conditions_page,policy,return_,about,get_products
from accounts.views import login_page,RegisterView,guest_register_view
from search.views import SearchProductView
from addresses.views import checkout_address_create_view
from django.views.generic import TemplateView,RedirectView


urlpatterns = [
    url(r'^$', home_page, name='index'),
    url('admin/', admin.site.urls),
    url('applogin/', login_page, name='login'),
    url('checkout/address/create/', checkout_address_create_view, name='checkout_address_create'),
    url('register/guest', guest_register_view, name='guest_register'),
    url('logout/', LogoutView.as_view(), name='logout'),
    url('register/', RegisterView, name='register'),
    url('contact/', contact_page, name='contact'),
    url('TAC/', conditions_page, name='TAC'),
    url('about/', about, name='about'),
    url('policy/', policy, name='policy'),
    url('return/', return_, name='returnpolicy'),
    url('accessories/', access, name='accessories'),
    url('search/',SearchProductView.as_view(), name='search'),
    url(r'^cart/', include(("cart.urls",'carts'), namespace='cart')),
    url(r'^billing/', include(("billing.urls",'billing'), namespace='billing')),
    url(r'^products/', include(("products.urls",'products'), namespace='products')),
    url(r'^orders/', include(("orders.urls",'orders'), namespace='orders')),
    # url('temp', TemplateView.as_view(template_name="socialapp/login1.html")),
    # url(r'accounts/', include('allauth.urls')),
    url(r'^accounts/$', RedirectView.as_view(url='/account')),
    url(r'^account/', include(("accounts.urls",'account'), namespace='account')),
    url(r'^accounts/', include("accounts.passwords.urls")),
    url(r'^filter/(?P<category>[\w-]+)/$', get_products, name='category'),
    
    # url(r'^password/change/done/$',
    #         auth_views.PasswordChangeDoneView.as_view(), 
    #         name='password_change_done'),
    # url(r'^password/reset/$', 
    #         auth_views.PasswordResetView.as_view(template_name = "registeration/password_reset_form.html"), 
    #         name='password_reset'),
    # url(r'^password/reset/done/$', 
    #         auth_views.PasswordResetDoneView.as_view(template_name = "registeration/password_reset_done.html"), 
    #         name='password_reset_done'),
    # url(r'^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 
    #         auth_views.PasswordResetConfirmView.as_view(template_name = "registeration/password_reset_confirm.html"), 
    #         name='password_reset_confirm'),
    # url(r'^password/reset/complete/$', 
    #         auth_views.PasswordResetCompleteView.as_view(template_name = "registeration/password_reset_complete.html"), 
    #         name='password_reset_complete'),

]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    #print(urlpatterns)
