from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from analytics.mixins import ObjectViewedMixin
from math import ceil
from .models import Product
from cart.models import Cart
from django.forms.models import model_to_dict
from django.core.serializers import serialize
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.safestring import mark_safe
import jsonpickle
from json import JSONEncoder


def ProductListView(request):
    allProds = Product.objects.all()

    print(type(allProds))
    context = {
        'allProds': allProds, 
    }
    print(allProds)
    return render(request, "products/parts.html", context)


def ProductPriceSort(request):
    sub_category = request.POST.getlist('checks')
    print(sub_category)
    filter_price1 = request.POST.get('min')
    filter_price2 = request.POST.get('max')
    category    = request.POST.get("category")
    # prod_array = product.objects.filter(category = 'category')
    print("%%%%")
    # data =list(prod_array)
    # print(type(data))
    if filter_price1 =='':
        filter_price1=0
    if filter_price2=='':
        filter_price2=Product.objects.all().aggregate(Max('price'))
   
    allProds = Product.objects.filter(price__range=(filter_price1,filter_price2),category=category)
   
    jsonData=serialize('json', allProds)
    print(jsonData)
    
    # qs = Product.objects.filter(int(price)>=min_price, active=True)
    print(filter_price1, filter_price2)
    print("*********")
    print(allProds)
    context ={'allProds':allProds}
    return render(request, "products/parts.html",context)

def ProductListView2(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats ={item['category'] for item in catprods}
    print("%%%%%%",cats)
    cats=sorted(cats)
    print("category",cats)
    for cat in cats:
        product = Product.objects.filter(category=cat)
        # n= len(product)
        # print("*****",product,"**",n)
        # nslides= n//4+ceil((n/4)-(n//4))
        allProds.append(product)
    print(allProds)
    context ={'allProds':allProds}
    # queryset = Product.objects.all()
    # context = {
    #     'object_list': queryset
    # }
    return render(request, "products/gears.html", context)

def ProductListView3(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats ={item['category'] for item in catprods}
    print("%%%%%%",catprods)
    cats=sorted(cats)
    print("category",cats)
    for cat in cats:
        product = Product.objects.filter(category=cat)
        # n= len(product)
        # print("*****",product,"**",n)
        # nslides= n//4+ceil((n/4)-(n//4))
        allProds.append(product)
    print(allProds)
    context ={'allProds':allProds}
    # queryset = Product.objects.all()
    # context = {
    #     'object_list': queryset
    # }
    return render(request, "products/bikes.html", context)

def SingleView(request, slug=None, *args, **kwargs):
    try:
        instance = Product.objects.get(slug=slug, active=True)
    except Product.DoesNotExist:
        raise Http404("Not found..")
    except Product.MultipleObjectsReturned:
        qs = Product.objects.filter(slug=slug, active=True)
        instance = qs.first()
    except:
        raise Http404("Uhhmmm")
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats ={item['category'] for item in catprods}
    for cat in cats:
        product = Product.objects.filter(category=cat)
        n= len(product)
        nslides= n//4+ceil((n/4)-(n//4))
        allProds.append([product,range(1, nslides),nslides])
    print("0th prod:",allProds[0])
    context ={'allProds':allProds,'object': instance, 'loop_times':range(0,4)}
    return render(request, "products/single.html", context)
     


    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductListView, self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context


# def ProductSlideView(request):
#     # queryset = Product.objects.all()
#     # print(queryset)
#     allProds = []
#     catprods = Product.objects.values('category', 'id')
#     cats ={item['category'] for item in catprods}
#     for cat in cats:
#         product = Product.objects.filter(category=cat)
#         n= len(product)
#         print("*****",product,"**",n)
#         nslides= n//4+ceil((n/4)-(n//4))
#         allProds.append([product,range(1, nslides),nslides])
#     print(allProds)
#     context ={'allProds':allProds}
#     return render(request, "products/css.html", context)
# def product_list_view(request):
#     queryset = Product.objects.all()
#     context = {
#         'object_list': queryset
#     }
#     return render(request, "products/list.html", context)


# class ProductDetailView(ObjectViewedMixin,DetailView):
#     queryset = Product.objects.all()
#     template_name = "products/single.html"

#     def SingleView(self, *args, **kwarg):
#         allProds = []
#         catprods = Product.objects.values('category', 'id')
#         cats ={item['category'] for item in catprods}
#         for cat in cats:
#             product = Product.objects.filter(category=cat)
#             n= len(product)
#             print("*****",product,"**",n)
#             nslides= n//4+ceil((n/4)-(n//4))
#             allProds.append([product,range(1, nslides),nslides])
#         print(allProds)
#         context ={'allProds':allProds}
#         return context
        
#     def get_context_data(self, *args, **kwargs):
#         context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
#         print(context)
#         # context['abc'] = 123
#         return context

# def product_detail_view(request, pk=None, *args, **kwargs):
#     #instance = Product.objects.get(pk=pk) #id
#     instance = get_object_or_404(Product, pk=pk)
#     print(instance)
#     context = {
#         'object': instance
#     }
#     return render(request, "products/single.html", context)

# class Views(ListView):
#     # queryset = Product.objects.all()
#     q = Product.objects.filter(title=title)
#     template_name = "products/list.html"


