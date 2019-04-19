from django.contrib import admin
from .models import Attributes, Item, Purchase, Type, PurchaseItem

# Register your models here.
admin.site.register([Attributes, Item, Purchase, Type, PurchaseItem])