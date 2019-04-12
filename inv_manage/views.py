from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.cache import never_cache

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
    return check_auth(request, 'inv_manage/neworder.html')
    #return render(request, page)

@never_cache
def inv_manage(request):
    return check_auth(request, 'inv_manage/inventory.html')
    #return render(request, 'inv_manage/inventory.html')

@never_cache
def previous_orders(request):
    return check_auth(request, 'inv_manage/orders.html')
    #return render(request, 'inv_manage/orders.html')

@never_cache
def add_item(request):
    types = Type.objects.all()
    if request.method == 'POST':
        db_methods.add_item(atts=request.POST)
        messages.success(request, 'Item has been successfully added.')
    return check_auth(request, "inv_manage/add_item.html", context={'types':types})
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