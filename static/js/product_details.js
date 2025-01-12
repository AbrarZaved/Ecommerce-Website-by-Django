console.log("hello");

document.addEventListener("DOMContentLoaded", function () {
  var priceElement = document.getElementById("price");
  var price = parseInt(priceElement.getAttribute("data-price"));
  // Function to calculate the new price based on the selected size
  function calculatePrice(size, oldPrice) {
    let priceIncrease = 0;
    switch (size) {
      case "M":
        priceIncrease = 200;
        break;
      case "L":
        priceIncrease = 300;
        break;
      case "XL":
        priceIncrease = 350;
        break;
      case "XXL":
        priceIncrease = 400;
        break;
      case "S":
      default:
        priceIncrease = 0;
        break;
    }
    return oldPrice + priceIncrease;
  }

  document.querySelectorAll("#sizes input[type='radio']").forEach((element) => {
    element.addEventListener("click", function () {
      let size = this.value;
      let newPrice = calculatePrice(size, price);
      priceElement.textContent = `Price: $${newPrice}`;
    });
  });
});
