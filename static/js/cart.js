// Create event handler for each button

//retrieve all buttons from "udpate-cart"
var updateBtns = document.getElementsByClassName("update-cart");

//for loop to loop through each button
for (var i = 0; i < updateBtns.length; i++) {
  // add eventlistener on click event
  updateBtns[i].addEventListener("click", function () {
    var productId = this.dataset.product;
    var action = this.dataset.action;
    console.log("productId:", productId, "Action:", action);

    console.log("USER:", user);
    if (user == "AnonymousUser") {
      console.log("User is not authenticated");
    } else {
        updateUserOrder(productId, action);
    }
  });
}

const updateUserOrder = (productId, action) =>{
  console.log('User is authenticated, sending data...')
  var url = '/update_item/'
  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    }
    body.JSON.stringify({'productId':productId, 'action':action})
  }).then((response) =>{
    return response.json()
  }).then((data) =>{
    console.log('Data', data)
  })
}