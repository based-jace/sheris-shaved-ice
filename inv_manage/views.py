from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
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