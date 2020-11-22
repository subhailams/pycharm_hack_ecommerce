import random
import os
from django.db import models
from django.db.models import Q


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    # print(instance)
    #print(filename)
    new_filename = random.randint(1,3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "products/{new_filename}/{final_filename}".format(
            new_filename=new_filename, 
            final_filename=final_filename
            )

class ProductQuerySet(models.query.QuerySet):
    def search(self, query):
        lookups = (Q(title__icontains=query) | 
                  Q(description__icontains=query) |
                  Q(price__icontains=query))
        return self.filter(lookups).distinct()

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query)

# class Category(models.Model):
#     name = models.CharField(max_length=200)



class Product(models.Model):
    title           = models.CharField(max_length=120)
    detail          = models.TextField(default="Null")
    description     = models.TextField(max_length=200)
    slug            = models.SlugField(blank=True, unique=True)
    category        = models.CharField(max_length=120,default='')
    subcategory     = models.CharField(max_length=120,default='')
    quantity        = models.IntegerField(default=1, null=True)
    price           = models.DecimalField(decimal_places=2, max_digits=20, default=39.99)
    image           = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    active          = models.BooleanField(default=True)

    objects = ProductManager()

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    @property
    def name(self):
        return self.title