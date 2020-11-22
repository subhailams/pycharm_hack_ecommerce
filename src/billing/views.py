from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import BillingProfile
from addresses.forms import AddressForm
from accounts.models import GuestEmail
from orders.models import Order, OrderConfirmation
from cart.models import Cart
from .Checksum import generate_checksum, verify_checksum
from products.models import Product
from addresses.models import Address
import sys
import razorpay
client = razorpay.Client(auth=("rzp_live_YZbvhRh0dOKiAS", "untpMRoqObXpppl55AmETt8q"))
# rzp_live_vTFPJKKdWndqOM      0lPkXJif7P6kCIfSv1MNXeQ8
order_id = None
cart_Id = None
GLOBAL_Entry = None
def razor_pay(request,id=None,*args, **kwargs):
	if request.method == 'GET':
		shipping_address_id = request.session.get("shipping_address_id", None)
		print("Session:",shipping_address_id)
		cart_obj, cart_created = Cart.objects.new_or_get(request)
		order_obj = None
		billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
		order_obj, order_obj_created= Order.objects.new_or_get(billing_profile, cart_obj)
		global order_id, cart_Id, GLOBAL_Entry
		order_id=order_obj
		cart_Id=cart_obj
		order_amount = int(100 * cart_obj.total)
		print(order_amount)
		order_currency = 'INR'
		order_receipt = 'order_rcptid_11'
		response = client.order.create(dict(amount=order_amount, currency=order_currency, receipt=order_receipt, payment_capture='1'))
		order = response['id']
		order_status = response['status']
		order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
		print("CHeck:",shipping_address_id)
		shipping_address=order_obj.shipping_address.get_address()
		order_obj.address=shipping_address
		order_obj.save()
		print("shipAdrr:",shipping_address)
		del request.session["shipping_address_id"]
		
		
		if order_status=='created':
			context={
				"Order_total":order_amount,
				"Billing_address":billing_profile.email,
				"Order_id": order_obj,
				"order_id":order,
				'cart':cart_obj,
				'shipping_address':shipping_address,
			}
			return render(request, 'billing/confirm_order.html', context)
	return HttpResponse('<h1>Error in  create order function</h1>')

@csrf_exempt
def payment_status(request):
	# global cart_Id 
	# print("Cart:",cart_Id)
	# cart_obj, cart_created = Cart.objects.new_or_get(request)
	# order_id = None
	# billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
	
	order_obj = request.POST['order_id']
	cart = request.POST['cart_id']
	print("Cart2:",cart)
	
	# cart_id = Cart.objects.get(id=cart_Id)
	order_id= Order.objects.get(order_id=order_obj)	
	cart_id = Cart.objects.get(id=cart)
	print("Cart3:",cart_id)
	response = request.POST
	print(response)
	params_dict = {
        'razorpay_payment_id' : response['razorpay_payment_id'],
        'razorpay_order_id' : response['razorpay_order_id'],
        'razorpay_signature' : response['razorpay_signature']
    }
	try:
		status = client.utility.verify_payment_signature(params_dict)
		print("status:",status)
		print("Order:",order_id)
		order_id.status = "paid"
		cart_id.isordered=True
		cart_id.save()
		obj = OrderConfirmation.objects.create(billing_profile = order_id.billing_profile,order_id=order_id, email=order_id.billing_profile.email)
		obj.send_order_confirmation()
		print("Orderpaid:",order_id)
		order_id.save()
		print("4")
		context={
			'status': 'Payment Successful',
			'cart_id':cart_id
			}

		return render(request, 'billing/order_summary.html', context)

	
	except:
		print("Oops!", sys.exc_info()[0], "occurred.")
		context={
		'status': 'Payment Failure!',
		'cart_id':cart_id
		}
		return render(request, 'billing/order_summary.html',context)

def cash_on_delivery(request):
	cart_obj, cart_created = Cart.objects.new_or_get(request)
	order_id = None
	billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
	order_id, order_obj_created= Order.objects.new_or_get(billing_profile, cart_obj)
	cart_obj.isordered=True
	cart_obj.save()
	order_id.cash_on_delivery=True
	order_id.status = "COD"
	order_id.save()
	obj = OrderConfirmation.objects.create(billing_profile = order_id.billing_profile,order_id=order_id, email=order_id.billing_profile.email)
	obj.send_order_confirmation()
	del request.session['cart_id']
	request.session['cart_items'] = 0
	context = {
		'status': 'Payment Successful'
	}
	return render(request,'billing/order_summary.html',context)
# merchant_key = settings.PAYTM_SECRET_KEY

# order_id = None
# cart_items=None
# req = None
# cart_id = None
# GLOBAL_Entry = None
# Create your views here.
# def initiate_payment(request):
# 	if request.method == 'GET':
# 		cart_obj, cart_created = Cart.objects.new_or_get(request)
# 		order_obj = None
# 		billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
# 		order_obj, order_obj_created= Order.objects.new_or_get(billing_profile, cart_obj)
# 		global order_id, cart_id, cart_items, req, GLOBAL_Entry
# 		order_id=order_obj
# 		cart_id=cart_obj
# 		request.session['cart_items'] = 0
# 		del request.session['cart_id']
# 		print("Order:",order_obj)
# 		print("cart_obj",cart_obj)
# 		# print(order_obj,cart_obj.total,billing_profile.email)
# 		param_dict = {
# 		'MID': settings.PAYTM_MERCHANT_ID,
# 		'ORDER_ID': str(order_obj),
# 		'CUST_ID': str(billing_profile.email),
# 		'TXN_AMOUNT': str(cart_obj.total),
# 		'CHANNEL_ID': settings.PAYTM_CHANNEL_ID,	
# 		'WEBSITE': settings.PAYTM_WEBSITE,
# 		# ('EMAIL', request.user.email),
# 		# ('MOBILE_N0', '9911223388'),
# 		'INDUSTRY_TYPE_ID': settings.PAYTM_INDUSTRY_TYPE_ID,
# 		'CALLBACK_URL': 'https://enduro2020.herokuapp.com/billing/callback/',
# 		# ('PAYMENT_MODE_ONLY', 'NO'),
# 		}
		
# 		param_dict['CHECKSUMHASH'] = generate_checksum(param_dict, merchant_key)
# 		return render(request,"billing/paytm.html",{'param_dict': param_dict})

# @csrf_exempt
# def callback(request):
	
# 	form=request.POST
# 	response_dict={}
# 	for i in form.keys():
# 		response_dict[i] = form[i]
# 		print("response:",i,response_dict[i])
# 		if i == 'CHECKSUMHASH':
# 			checksum = form[i]
	
# 	verify = verify_checksum(response_dict, merchant_key ,checksum)
	
# 	if verify:
# 		if response_dict['RESPCODE'] == '01':
		
# 			cart_obj,cart_created = Cart.objects.new_or_get(request)
# 			billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
		
# 			print('Order Successful')
# 			global order_id
# 			order_obj=order_id
# 			order_obj.mark_paid()
# 			obj = OrderConfirmation.objects.create(billing_profile = order_obj.billing_profile,order_id=order_obj,email=order_obj.billing_profile.email)
# 			obj.send_order_confirmation()
# 			order_obj.save()
# 			global cart_id
# 			cart_id=cart_id
# 		else:
# 			print('Order was not successful because' + response_dict['RESPMSG'])
# 	return render(request, 'carts/checkout-done.html', {'response': response_dict})


