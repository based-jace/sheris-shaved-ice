from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

def check_auth(request):
    if request.user.is_authenticated:
        pass
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

def home(request):
    if request.user.is_authenticated:
        return render(request, 'inv_manage/home.html')
    else:
        return login_user(request)

def neworder(request):
    check_auth(request)
    return HttpResponse("Enter order info here.")

def inv_manage(request):
    check_auth(request)
    return HttpResponse("View and edit current inventory here.")

def previous_orders(request):
    check_auth(request)
    return HttpResponse("View past orders here.")

def add_item(request):
    check_auth(request)
    return HttpResponse("Add a new item to the database here.") 
        # This is ambiguous, because it's not strictly "items" able to be added, but anything in the database,
        #   including categories.

def edit_item(request):
    check_auth(request)
    return HttpResponse("Edit database items.") 
        # "items" here fits the same definition as that above. This might be able to be combined with the
        #   page above.