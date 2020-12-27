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
      console.log("User is authenticated, sending data...");
    }
  });
}
