import json
from .models import *

# cookiecart function that takes in request and return a dictionary
def cookieCart(request):
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
  return {'cartItems': cartItems, 'order': order, 'items': items}
  
def cartData(request):
  if request.user.is_authenticated:
    # connects user to customer
    customer = request.user.customer
    # connects customer's order
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    # get items attached to order
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items
  else:
    cookieData = cookieCart(request)
    cartItems = cookieData['cartItems']
    order = cookieData['order']
    items = cookieData['items']
  return {'cartItems': cartItems, 'order': order, 'items': items}

def guestOrder(request, data):
    print('User is not logged in')
    print('COOKIES:', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

      # if email exists, attach to customer and can see how many times they have shopped with us even if they have not created a login account. Able to see all previous orders.
    customer, created = Customer.objects.get_or_create(
      email = email,
    )
    customer.name = name
    customer.save()

    order = Order.objects.create(
      customer=customer,
      complete=False,
    )
    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
          )
    return customer, order