from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.http import Http404
import json
from django.db.models.functions import Lower

from . import password_reset

# Forgot password reset
import secrets

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
        context = {
            "active":"home", 
            "json_items":"",
            "recent_purchases": Purchase.objects.all().order_by('-id')[:5],
            "low_inventory":{},
            "json_items":{}
        }
        context["low_inventory"] = Item.objects.exclude(item_id__type_id__name = 'Syrup').filter(quantity__lt = 100, available=True)
        context["json_items"] = db_methods.jsonify_items(context["low_inventory"])
        return render(request, 'inv_manage/home.html', context=context)
    else:
        return login_user(request)

@never_cache
def forgot_password(request):
    if request.method == 'POST':
        if request.POST:
            email = request.POST['emailaddress']
            try:
                this_user = User.objects.get(email=email)
                password_reset.send_link(this_user)
                messages.success(request, 'Check your email for further instructions.')
            except:
                messages.error(request, 'User not found')
            
    return render(request, 'inv_manage/forgotpassword.html')

@never_cache
def reset_password(request, reset_key):
    if request.method == 'POST':
        try:
            password_reset.new_password(reset_key, request.POST['password'])
            messages.success(request, 'Password successfully changed')
        except:
            messages.error('Something went wrong')
        return redirect('inv_manage:home')
    if not password_reset.test_key(reset_key):
        messages.error(request, 'Your key is invalid.')
        return redirect('inv_manage:home')
    return render(request, 'inv_manage/resetpassword.html')

@never_cache
def neworder(request):
    items = Item.objects.filter(available=True) 
    orders = PurchaseItem.objects.all()

    if request.method == 'POST':
        atts = dict(request.POST)
        db_methods.neworder(atts)
        messages.success(request, 'Order has been successfully added.')

    return check_auth(request, 'inv_manage/neworder.html',context={'items':items,'orders':orders})

@never_cache
def inv_manage(request):
    #items = {}
    items = Item.objects.filter(available=True).order_by(Lower('item_id'))
    context = {
        'items': items, 
        'json_items': db_methods.jsonify_items(items), 
        'active':'inventory'
    }

    if request.method == "POST":
        db_methods.delete_selected(request.POST)

    return check_auth(request, 'inv_manage/inventory.html',context=context)

@never_cache
def previous_orders(request):
    purchases = Purchase.objects.all()
    context = {
        'purchases':purchases, 
        'active':'orders', 
        'json_items':db_methods.jsonify_orders(purchases)
    }
    if request.method == "POST":
        print(request.POST)
        db_methods.delete_orders(request.POST)
    return check_auth(request, 'inv_manage/orders.html', context=context)
        
#Adding an attribute       
# attribute = Attributes.objects.create(type_id=types[int(request.POST.get('typename'))])
# attribute.name = request.POST.get('attname')
# attribute.save()
# attributes = Attributes.objects.all()
# print(attributes)

@never_cache
def add_item(request):
    types = Type.objects.all()
    
    if request.method == 'POST':
        db_methods.add_item(atts=request.POST)
        messages.success(request, 'Item has been successfully added.')

    return check_auth(request, "inv_manage/add_item.html", context={'types':types})

@never_cache
def edit_item(request, item_id):
    types = Type.objects.all()
    try:
        item = Item.objects.get(pk=item_id)
    except Item.DoesNotExist:
        raise Http404("Item is not in the inventory")

    if request.method == 'POST':
        db_methods.edititem(atts=request.POST,item_id=item_id)
        messages.success(request, 'Item has been successfully updated.')
        return redirect('inv_manage:inventory')

    return check_auth(request,'inv_manage/edititem.html',context={'item':item,'types':types})
    
        # "items" here fits the same definition as that above. This might be able to be combined with the
        #   page above.

@never_cache
def add_type(request):
    types = Type.objects.all()
    if request.method == "POST":
        db_methods.create_type(request.POST)
        name = types[len(types)-1].name
        return JsonResponse({
            'name':name,
            'id':types[len(types)-1].id,
            'message': 'New type, ' + name + ', has been successfully added'
        })

@never_cache
def edit_order(request,order_id):
    items = Item.objects.all()
    purchase = Purchase.objects.get(id=order_id)
    try:
        orders = PurchaseItem.objects.filter(purchase_id=purchase)
    except PurchaseItem.DoesNotExist:
        raise Http404("Order does not exist.")
    
    if request.method == "POST":
        db_methods.editorder(atts=request.POST, purchase=purchase)
        messages.success(request, 'Order has successfully been updated.')
        return redirect('inv_manage:orders')

    return check_auth(request,'inv_manage/editorder.html',context={'items':items,'orders':orders})
