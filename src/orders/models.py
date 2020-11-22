import math
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save,post_save
from billing.models import BillingProfile
from cart.models import Cart
from addresses.models import Address
from ecommerce.utils import unique_order_id_generator
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import get_template
ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),
    ('COD','CashOnDelivery'),
)
class OrderManagerQuerySet(models.query.QuerySet):
    def by_request(self, request):
        billing_profile, created = BillingProfile.objects.new_or_get(request)
        print("love:",self.filter(billing_profile=billing_profile))
        return self.filter(billing_profile=billing_profile)
        

    def not_created(self):
        print("hate:",self.exclude(status='created'))
        return self.exclude(status='created')

class OrderManager(models.Manager):
        def get_queryset(self):
            return OrderManagerQuerySet(self.model, using=self._db)

        def by_request(self, request):
            return self.get_queryset().by_request(request)

        def new_or_get(self, billing_profile, cart_obj):
            created = False
            qs = self.get_queryset().filter(
                    billing_profile=billing_profile, 
                    cart=cart_obj, 
                    active=True,
                    status='created')
            if qs.count() == 1:
                obj = qs.first()
            else:
                obj = self.model.objects.create(
                        billing_profile=billing_profile, 
                        cart=cart_obj)
                created = True
            return obj, created





class Order(models.Model):
    billing_profile  = models.ForeignKey(BillingProfile ,null=True,blank=True,on_delete=models.CASCADE)
    order_id         = models.CharField(max_length=120, blank=True) # AB31DE3 
    shipping_address = models.ForeignKey(Address, related_name="shipping_address",null=True, blank=True,on_delete=models.CASCADE)
    # billing_address  = models.ForeignKey(Address, related_name="billing_address", null=True, blank=True,on_delete=models.CASCADE)
    address          = models.CharField(max_length=120, default="Chennai")
    cart             = models.ForeignKey(Cart,on_delete=models.CASCADE)
    status           = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    shipping_total   = models.DecimalField(default=5.99, max_digits=100, decimal_places=2)
    total            = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    active           = models.BooleanField(default=True)
    updated          = models.DateTimeField(auto_now=True)
    timestamp        = models.DateTimeField(auto_now_add=True,blank=True)
    being_delivered  = models.BooleanField(default=False)
    received         = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted   = models.BooleanField(default=False)
    cash_on_delivery = models.BooleanField(default=False)

    def __str__(self):
        return self.order_id

    objects = OrderManager()  

    class Meta:
       ordering = ['-timestamp', '-updated']

    def get_absolute_url(self):
        return reverse("orders:detail", kwargs={'order_id': self.order_id})

    def get_status(self):
        if self.status == "refunded":
            return "Refunded order"
        elif self.status == "shipped":
            return "Shipped"
        return "Shipping Soon"  


    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        new_total = math.fsum([cart_total, shipping_total])
        formatted_total = format(new_total, '.2f')
        self.total = formatted_total
        self.save()
        return new_total

    def check_done(self):
        billing_profile = self.billing_profile
        shipping_address = self.shipping_address
        billing_address = self.billing_address
        total   = self.total
        if billing_profile and shipping_address and billing_address and total > 0:
            return True
        return False

    def mark_paid(self):
        self.status = "paid"
        self.save()
        return self.status

def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)
    qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=False)
    

pre_save.connect(pre_save_create_order_id, sender=Order)

def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.total
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()

post_save.connect(post_save_cart_total, sender=Cart)


def post_save_order(sender, instance, created, *args, **kwargs):
    print("running")
    if created:
        print("Updating... first")
        instance.update_total()


post_save.connect(post_save_order, sender=Order)

class OrderConfirmQuerySet(models.query.QuerySet):
    def by_request(self, request):
        billing_profile, created = BillingProfile.objects.new_or_get(request)
        return self.filter(billing_profile=billing_profile)

class OrderConfirmationManager(models.Manager):
    def get_queryset(self):
        return OrderConfirmQuerySet(self.model, using=self._db)

class OrderConfirmation(models.Model):
    billing_profile = models.ForeignKey(BillingProfile ,null=True,blank=True,on_delete=models.CASCADE)
    order_id        = models.CharField(max_length=120, blank=True) 
    email           = models.EmailField()

    
    objects = OrderConfirmationManager()

    def __str__(self):
        return self.order_id

    def send_order_confirmation(self):
        base_url = getattr(settings, 'BASE_URL')
        # key_path = reverse("account:email-activate", kwargs={'key': self.key}) # use reverse
        # path = "{base}{path}".format(base=base_url, path=key_path)
        context = {
            # 'path': path,
            'email': self.billing_profile.email,
            'order_id': self.order_id,
          

        }
        txt_ = get_template("orders/order_confirm.txt").render(context)
        html_ = get_template("orders/order_confirm.html").render(context)
        subject = 'Order Confirmation'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [self.billing_profile.email]
        sent_mail = send_mail(
                    subject,
                    txt_,
                    from_email,
                    recipient_list,
                    html_message=html_,
                    fail_silently=False,
            )
        return sent_mail


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"

class RefundGrandQuerySet(models.query.QuerySet):
    def by_request(self, request):
        billing_profile, created = BillingProfile.objects.new_or_get(request)
        return self.filter(billing_profile=billing_profile)

class RefundGrandManager(models.Manager):
    def get_queryset(self):
        return OrderConfirmQuerySet(self.model, using=self._db)

class RefundGrandConfirmation(models.Model):
    # billing_profile = models.ForeignKey(BillingProfile ,null=True,blank=True,on_delete=models.CASCADE)
    order_id        = models.CharField(max_length=120, blank=True) 
    email           = models.EmailField()
    timestamp       = models.DateTimeField(auto_now_add=True)
    update          = models.DateTimeField(auto_now=True)

    objects = RefundGrandManager()

    def __str__(self):
        return self.order_id

    def send_refund_granted(self):
        base_url = getattr(settings, 'BASE_URL')
        # key_path = reverse("account:email-activate", kwargs={'key': self.key}) # use reverse
        # path = "{base}{path}".format(base=base_url, path=key_path)
        context = {
            # 'path': path,
            'email': self.email,
            'order_id': self.order_id
        }
        txt_ = get_template("orders/refund_req_confirm.txt").render(context)
        html_ = get_template("orders/refund_req_confirm.html").render(context)
        subject = 'Order Confirmation'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [self.email]
        sent_mail = send_mail(
                    subject,
                    txt_,
                    from_email,
                    recipient_list,
                    html_message=html_,
                    fail_silently=False,
            )
        return sent_mail

def post_save_refund_granted(sender, instance,*args, **kwargs):
    # print("Ins:",instance, instance.billing_profile, instance.billing_profile.email)
    obj = RefundGrandConfirmation.objects.create( order_id=instance, email=instance.email)
    obj.send_refund_granted()

post_save.connect(post_save_refund_granted, sender=Refund)   