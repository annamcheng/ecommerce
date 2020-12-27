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
	context = {'items':items}
	return render(request, 'store/cart.html', context)

def checkout(request):
	context = {}
	return render(request, 'store/checkout.html', context)