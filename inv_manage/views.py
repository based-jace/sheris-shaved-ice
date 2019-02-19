from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def inv_manage(request):
    return HttpResponse("Hello, world.")
	#return render(request, 'Hello World')