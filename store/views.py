from django.shortcuts import render
from django.http import JsonResponse
from .models import *

# Create views here
def store(request):
	# get all products
	products = Product.objects.all()
	# pass into context
	context = {'products':products}
	return render(request, 'store/store.html', context)

def cart(request):
	if request.user.is_authenticated:
		# connects user to customer
		customer = request.user.customer
		# connects customer's order
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		# get items attached to order
		items = order.orderitem_set.all()
	else:
		# return empty value if customer is not logged in/authenticated
		items = []
		order = {'get_cart_total': 0, 'get_cart_items': 0}
		
	context = {'items':items, 'order':order}
	return render(request, 'store/cart.html', context)

def checkout(request):
	if request.user.is_authenticated:
		# connects user to customer
		customer = request.user.customer
		# connects customer's order
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		# get items attached to order
		items = order.orderitem_set.all()
	else:
		# return empty value if customer is not logged in/authenticated
		items = []
		order = {'get_cart_total': 0, 'get_cart_items': 0}
		
	context = {'items':items, 'order':order}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	return JsonResponse('Item was added', safe=False)