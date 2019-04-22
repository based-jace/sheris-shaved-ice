from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.http import Http404
#from django.shortcuts import get_object_or_404
#from decimal import Decimal
#import datetime
import json

from .databaseutils import db_methods

from .models import Type, Attributes, Item, Purchase, PurchaseItem

# Create your views here.

def check_auth(request, page, context=None): # Redirects to login if not authorized
                                             # This prevents you from being able to go back
                                             # And view info if not logged in
    if request.user.is_authenticated:
        return render(request, page, context)
    else:
        return redirect('inv_manage:home')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ('You have successfully logged in.'))
        else:
            messages.error(request, ('Your username and/or password are invalid.'))
        return redirect('inv_manage:home')
    else:
        return render(request, 'authentication/login.html')

def logout_user(request):
    logout(request)

    messages.success(request, ('You have been successfully logged out.'))
    return redirect('inv_manage:home')

@never_cache
def home(request):
    if request.user.is_authenticated:
        return render(request, 'inv_manage/home.html', context={"active":"home"})
    else:
        return login_user(request)

@never_cache
def neworder(request):
    items = Item.objects.filter(available=True) 
    orders = PurchaseItem.objects.all()

    if request.method == 'POST':
        atts = dict(request.POST)
        db_methods.neworder(atts)

    return check_auth(request, 'inv_manage/neworder.html',context={'items':items,'orders':orders})

# @never_cache
# def inv_manage(request):
#     items = Item.objects.filter(available=True)

#     if request.method == "POST":
#         db_methods.delete_selected(request.POST)

#     return check_auth(request, 'inv_manage/inventory.html',context={'items':items, 'active':'inventory'})

@never_cache
def inv_manage(request):
    items = Item.objects.filter(available=True)

    if request.method == "POST":
        db_methods.delete_selected(request.POST)
    print(items)
    context = {'items': items, 'json_items': db_methods.jsonify_items(items), 'active':'inventory'}
    return check_auth(request, 'inv_manage/inventory.html',context=context)

@never_cache
def previous_orders(request):
    purchases = Purchase.objects.all()
    return check_auth(request, 'inv_manage/orders.html', context={'purchases':purchases, 'active':'orders'})
        
#Adding an attribute       
# attribute = Attributes.objects.create(type_id=types[int(request.POST.get('typename'))])
# attribute.name = request.POST.get('attname')
# attribute.save()
# attributes = Attributes.objects.all()
# print(attributes)

@never_cache
def add_item(request):
        # This is ambiguous, because it's not strictly "items" able to be added, but anything in the database,
        # including categories.

    types = Type.objects.all()
    
    if request.method == 'POST':
        db_methods.add_item(atts=request.POST)
        messages.success(request, 'Item has been successfully added.')

    return check_auth(request, "inv_manage/add_item.html", context={'types':types})
  
    '''
    #Grabs all possible attributes out of the database
    attributes = Attributes.objects.all() 
    #if the user hits submit creates an item and saves it to the database   
    if request.method == 'POST':
        item = Item.objects.create(item_id=attributes[int(request.POST.get('attname'))],quantity=int(request.POST.get('quantity')))        
        item.save()
        return render(request,'inv_manage/additem.html',{'attributes':attributes})
        #return redirect('inv_manage:orders')
    else:    
        return render(request,'inv_manage/additem.html',{'attributes':attributes})
    '''

@never_cache
def edit_item(request, item_id):
    #return check_auth(request)
    types = Type.objects.all()
    try:
        item = Item.objects.get(pk=item_id)
    except Item.DoesNotExist:
        raise Http404("Item is not in the inventory")

    if request.method == 'POST':
        db_methods.edititem(atts=request.POST,item_id=item_id,attribute_id=item.item_id.id)
        messages.success(request, 'Item has successfully been updated.')
        return redirect('inv_manage:inventory')

    return check_auth(request,'inv_manage/edititem.html',context={'item':item,'types':types})
    
        # "items" here fits the same definition as that above. This might be able to be combined with the
        #   page above.

@never_cache
def add_type(request):
    if request.method == "POST":
        return JsonResponse({'message':'Thank You'})

@never_cache
def edit_order(request,order_id):
    items = Item.objects.filter(available=True)
    purchase = Purchase.objects.get(id=order_id)
    try:
        orders = PurchaseItem.objects.filter(purchase_id=purchase)
    except PurchaseItem.DoesNotExist:
        raise Http404("Order does not exist.")
    
    if request.method == "POST":
        db_methods.editorder(atts=request.POST,orders=orders,purchase=purchase)
        messages.success(request, 'Order has successfully been updated.')
        return redirect('inv_manage:orders')

    return check_auth(request,'inv_manage/editorder.html',context={'items':items,'orders':orders})
