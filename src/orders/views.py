from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.views.generic import ListView, DetailView, View
from django.shortcuts import render,redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from billing.models import BillingProfile
from .models import Order, Refund
from .forms import RefundForm

class OrderListView(LoginRequiredMixin, ListView):

    def get_queryset(self):
        print(Order.objects.by_request(self.request).not_created())
        return Order.objects.by_request(self.request).not_created()


class OrderDetailView(LoginRequiredMixin, DetailView):
    
    def get_object(self):
        #return Order.objects.get(id=self.kwargs.get('id'))
        #return Order.objects.get(slug=self.kwargs.get('slug'))
        qs = Order.objects.by_request(
                    self.request
                ).filter(
                    order_id = self.kwargs.get('order_id')
                )
        if qs.count() == 1:
            return qs.first()
        raise Http404

class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {
            'form': form
        }
        return render(self.request, "orders/request_refund.html", context)

    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            order_id = form.cleaned_data.get('order_id')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            # edit the order
            print("Order:",order_id,message)
            try:
                order_obj = Order.objects.get(order_id=order_id)
                if email != order_obj.billing_profile.email:
                    messages.error(self.request, "Email is incorrect.")
                    return redirect("orders:request-refund")
                order_obj.refund_requested = True
                order_obj.save()

                # store the refund
                refund = Refund()
                refund.order = order_obj
                refund.reason = message
                refund.email = email
                refund.save()
                
                messages.error(self.request, "Your request was received.")
                return redirect("orders:request-refund")

            except ObjectDoesNotExist:
                messages.error(self.request, "This order does not exist.")
                return redirect("orders:request-refund")
