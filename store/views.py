from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime

from .models import *
from . utils import cookieCart

# Create views here
def store(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		# return empty value if customer is not logged in/authenticated
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']

	# get all products
	products = Product.objects.all()
	# pass into context
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)

def cart(request):
	if request.user.is_authenticated:
		# connects user to customer
		customer = request.user.customer
		# connects customer's order
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		# get items attached to order
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		try: 
			cart = json.loads(request.COOKIES['cart'])
		except:
			cart = {}
		print('Cart:', cart)
		# return empty value if customer is not logged in/authenticated
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']

		# update cart number on cart page
		for i in cart:
			try:
				cartItems += cart[i]['quantity']
				# accessing product and price on cart page
				product = Product.objects.get(id=i)
				total = (product.price * cart[i]['quantity'])
				# accessing order total and items on cart page
				order['get_cart_total'] += total
				order['get_cart_items'] += cart[i]['quantity']
				# accesses item list on cart page
				item = {
					'product': {
						'id': product.id,
						'name': product.name,
						'price': product.price,
						'imageURL':product.imageURL
					},
					'quantity': cart[i]['quantity'],
					'get_total':total,
				}
				# append item dictionary to items list on cart page
				items.append(item)

				if product.digital == False:
					order['shipping'] = True
			except:
				pass
				
		# elements passed into context dictionary
	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
def checkout(request):
	if request.user.is_authenticated:
		# connects user to customer
		customer = request.user.customer
		# connects customer's order
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		# get items attached to order
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		# return empty value if customer is not logged in/authenticated
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		total = float(data['form']['total'])
		order.transaction_id = transaction_id
	
		if total == order.get_cart_total:
			order.complete = True
		order.save()

		if order.shipping == True:
			ShippingAddress.objects.create(
			customer=customer,
			order=order,
			address=data['shipping']['address'],
			city=data['shipping']['city'],
			state=data['shipping']['state'],
			zipcode=data['shipping']['zipcode'],
			)
	else:
		print('User is not logged in')

	return JsonResponse('Payment submitted..', safe=False)