from django.shortcuts import render
from .models import *

# Create views here
def store(request):
	# get all products
	products = Product.objects.all()
	# pass into context
	context = {'products':products}
	return render(request, 'store/store.html', context)

def cart(request):
	context = {}
	return render(request, 'store/cart.html', context)

def checkout(request):
	context = {}
	return render(request, 'store/checkout.html', context)