from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.shortcuts import get_object_or_404
from decimal import Decimal
import datetime

from .databaseutils import item_creation

from .models import Type,Attributes,Item,Purchase,PurchaseItem

from .models import Type
from .db_methods import db_methods

# Create your views here.

def check_auth(request, page, context=None):
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
    attributes = Attributes.objects.all() 
    #TODO Make it so you can enter multipe items at one time.
    #TODO Make it look cleaner
    if request.method == 'POST':
        purchase = Purchase()
        purchase.total_amount = 0.00
        #TODO set of a while loop to go through the different rows of orders.
        purchase.purchase_date = datetime.date.today()
        purchase.total_amount += float(request.POST.get('cost'))
        purchase.save()
        purchaseItem = PurchaseItem.objects.create(item_id=attributes[int(request.POST.get('attname'))],purchase_id=purchase,quantity=int(request.POST.get('quantity')),total_amount=Decimal(request.POST.get('cost')))
        purchaseItem.save()
        #Checks to see if there are any instances of the object in the datbase
        count = Item.objects.filter(item_id=purchaseItem.item_id).count()
        #Creates an item       
        item_creation(count,purchaseItem)

        return render(request, 'inv_manage/neworder.html',{'attributes':attributes})
    else:
        return render(request, 'inv_manage/neworder.html',{'attributes':attributes})
    #return render(request, page)

@never_cache
def inv_manage(request):
    items = Item.objects.all()
    #return check_auth(request, 'inv_manage/inventory.html')
    return render(request, 'inv_manage/inventory.html',{'items':items})

@never_cache
def previous_orders(request):
    orders = PurchaseItem.objects.all()
    #return check_auth(request, 'inv_manage/orders.html')
    return render(request, 'inv_manage/orders.html',{'orders':orders})
        
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

        # This is ambiguous, because it's not strictly "items" able to be added, but anything in the database,
        #   including categories.

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