from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def authentication(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('inv_manage:home')
        else:
            return redirect('inv_manage:login')
    else:
        return render(request, 'authentication/login.html')

def home(request):
    return HttpResponse("Welcome to the inventory overview.")

def neworder(request):
    return HttpResponse("Enter order info here.")

def inv_manage(request):
    return HttpResponse("View and edit current inventory here.")

def previous_orders(request):
    return HttpResponse("View past orders here.")

def add_item(request):
    return HttpResponse("Add a new item to the database here.") 
        # This is ambiguous, because it's not strictly "items" able to be added, but anything in the database,
        #   including categories.

def edit_item(request):
    return HttpResponse("Edit database items.") 
        # "items" here fits the same definition as that above. This might be able to be combined with the
        #   page above.