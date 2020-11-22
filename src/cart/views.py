from django.http import JsonResponse,HttpResponse
from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render,redirect
from django.utils.http import is_safe_url
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from billing.models import BillingProfile
from accounts.models import GuestEmail,User
from accounts.forms import LoginForm,GuestForm
from addresses.forms import AddressForm
from orders.models import Order
from .models import Cart,CartItem
from products.models import Product
from addresses.models import Address
from accounts.signals import user_logged_in


c = 0
import razorpay
client = razorpay.Client(auth=("rzp_test_fu6uylByoiLTWv", "UHCkK8GTEqFliNdSub9L3Vrd"))

def cart_detail_api_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = [{"id": x.id, "name": x.name, "price": x.price, "image": x.image.url} for x in cart_obj.products.all()] # [<object>, <object>, <object>]
    # products_list = []
    # for x in cart_obj.products.all():
    #     products_list.append(
    #             {"name": x.name, "price": x.price}
    #         )
    cart_data  = {"products": products, "subtotal": cart_obj.subtotal, "total": cart_obj.total}
    print(cart_data)
    return JsonResponse(cart_data)



def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    if cart_obj.isordered:
        print("*****")
        request.session['cart_items'] = 0
        del request.session['cart_id']
		
    return render(request, "carts/cart.html", {"cart": cart_obj})

def cart_update(request):
    product_id = request.POST.get('product_id')
    # print(product_id)
    try:
        qty = request.POST.get('qty')
        update_qty = True
    except:
        qty = None
        update_qty = False

    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print("Show message to user, product is gone?")
            return redirect("cart:cart")

        cart_obj, new_obj = Cart.objects.new_or_get(request)
        request.session['cart_id'] = cart_obj.id
        print("CCCart:",request.session['cart_id'],cart_obj)
        # cart_item, created = CartItem.objects.get_or_create(cart=cart_obj, product=product_obj)
        # if created:
        #     print("created")
  

        # print("Product",product_obj,cart_obj.cartitem_set.all())
        products = [ x.product.name for x in cart_obj.cartitem_set.all()] # [<object>, <object>, <object>]
        print("Prod Obj",product_obj)

        print("Prod Id",products)
        if str(product_obj) in products:
            cart_item = CartItem.objects.get(cart=cart_obj, product=product_obj)
            cart_item.delete()
            print("sss",product_obj)
            cart_obj.products.remove(product_obj)
            
            added = False
        else:
            cart_item, created = CartItem.objects.get_or_create(cart=cart_obj, product=product_obj)
            cart_obj.products.add(product_obj)
            # cart_item.add(product_obj)
            print("elseeee") 
            added = True
        
        if update_qty and qty:
            if int(qty) == 0:
                cart_item.delete()
            else:
                cart_item.quantity = qty
                cart_item.save()
        else: 
            pass
        new_total = 0.0
        for x in cart_obj.cartitem_set.all():
            line_item = float(x.product.price) * x.quantity
            cart_item.price= line_item
            new_total += line_item

        request.session['cart_items'] = cart_obj.cartitem_set.count()
        print("cartTotal:",cart_obj.cartitem_set.count())
        cart_obj.subtotal = new_total
        if cart_obj.subtotal > 0:
            cart_obj.total = Decimal(cart_obj.subtotal) 
            print("cart_total:",cart_obj.total)
        else :
            cart_obj.total = 0.00
        cart_obj.save()
        # return redirect(product_obj.get_absolute_url())
        print("---------------",request.is_ajax())
        if request.is_ajax(): # Asynchronous JavaScript And XML / JSON
            print("Ajax request")
            json_data = {
                "added": added,
                "removed": not added,
                "cartItemCount": cart_obj.cartitem_set.count()
            }
            return JsonResponse(json_data)
    return redirect("cart:cart")



def checkout_home(request):
    global c
    c+=1
    order_status = None
    print(c)
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.cartitem_set.count()== 0:
        return redirect("cart:cart")

    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    billing_address_id = request.session.get("billing_address_id", None)
    shipping_address_id = request.session.get("shipping_address_id", None)
    print("CHeck:",shipping_address_id)

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if billing_profile is not None:
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
  
    if shipping_address_id:
        order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
        print("CHeck:",shipping_address_id)
        order_obj.save()
        return redirect("billing:razor")
        # order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
        # print("CHeck:",shipping_address_id)
        # order_obj.save()
        # shipping_address=order_obj.shipping_address.get_address
        # order_amount = int(100 * cart_obj.total)
        # order_currency = 'INR'
        # order_receipt = 'order_rcptid_11'
        # response = client.order.create(dict(amount=order_amount, currency=order_currency, receipt=order_receipt, payment_capture='0'))
        # order = response['id']
        # order_status = response['status']
        # print("order razor:",order, order_status)
        # print("Order amt:",order_amount )
		# # print( order_obj.billing_profile.get_address)
        # if order_status=='created':
        #     context={
        #     "Order_total":order_amount,
        #     "Billing_address":billing_profile,
        #     "object": order_obj,
        #     "order_id":order,
        #     "cart": cart_obj,
        #     "shipping_address":shipping_address
            
        #     }
        #     return render(request, 'billing/confirm_order.html', context)
    
    context = {
            "cart_obj" : cart_obj,
            "object": order_obj,
            "billing_profile": billing_profile,
            "login_form": login_form,
            "guest_form": guest_form,
            "address_form":address_form
        }
    
    
     
    return render(request, "carts/checkout.html", context)
def checkout_done_view(request):
    return render(request, "carts/checkout-done.html", {})

def cart_login(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            user_logged_in.send(user.__class__, instance=user, request=request)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("cart:checkout")
        else:
            print("Error")
        
    return render(request, "accounts/index.html")


# @csrf_exempt
# def handlerequest(request):
#     return HttpResponse('done')
#     pass
