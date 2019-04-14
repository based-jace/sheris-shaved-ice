from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.cache import never_cache
#from django.shortcuts import get_object_or_404
#from decimal import Decimal
#import datetime

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
        return render(request, 'inv_manage/home.html')
    else:
        return login_user(request)

@never_cache
def neworder(request):
    attributes = Attributes.objects.all() # < Unnecessary? Can change to just item?
    #TODO Make it so you can enter multipe items at one time.
    if request.method == 'POST':
        atts = dict(request.POST)
        db_methods.neworder(atts)

    return check_auth(request, 'inv_manage/neworder.html',context={'attributes':attributes})

@never_cache
def inv_manage(request):
    items = Item.objects.all()
    return check_auth(request, 'inv_manage/inventory.html',context={'items':items})

@never_cache
def previous_orders(request):
    orders = PurchaseItem.objects.all()
    return check_auth(request, 'inv_manage/orders.html', context={'orders':orders})
        
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
def edit_item(request):
    #return check_auth(request)
    return HttpResponse("Edit database items.") 
        # "items" here fits the same definition as that above. This might be able to be combined with the
        #   page above.

@never_cache
def add_type(request):
    if request.method == "POST":
        return JsonResponse({'message':'Thank You'})