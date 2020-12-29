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
    return {'cartItems':cartItems, 'order':order, 'items':items}