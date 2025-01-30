document.addEventListener("DOMContentLoaded", function () {
  var priceElement = document.getElementById("price");
  var price = parseInt(priceElement.getAttribute("data-price"));
  var quantity = 1;
  document.getElementById("quantity").addEventListener("change", (e) => {
    quantity = parseInt(e.target.value) || 1;
  });
  console.log(quantity);
  var newPrice = price,
    size = "S";
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
      size = this.value;
      newPrice = calculatePrice(size, price);
      priceElement.textContent = `Price: $${newPrice}`;
    });
  });
  var cartButton = document.getElementById("add_cart");
  cartButton.addEventListener("click", (e) => {
    e.preventDefault();
    const cart_value = cartButton.getAttribute("data-value");

    fetch("http://127.0.0.1:8000/cart/add_cart", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ cart_value, newPrice, size, quantity }),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        const message = document.getElementById("message");
        message.innerHTML = ""; // Clear previous toasts
        if (data.success) {
          document.getElementById(
            "cart_item"
          ).textContent = `${data.total_item}`;
        }
        const toast = document.createElement("div");
        toast.classList.add("toast");
        toast.style.transition = "0.32s all ease-in-out";
        toast.style.position = "fixed";
        toast.style.bottom = "10px";
        toast.style.right = "10px";
        toast.style.color = "white";
        toast.style.opacity = "0";
        toast.style.padding = "0.5rem 1.5rem";
        toast.style.borderRadius = "0.25rem";
        toast.style.boxShadow = "0px 4px 8px rgba(0, 0, 0, 0.1)";
        toast.setAttribute("role", "alert");
        toast.setAttribute("aria-live", "assertive");
        toast.setAttribute("aria-atomic", "true");

        const isSuccess = data.success;
        toast.style.backgroundColor = isSuccess ? "#007bff" : "#077c7e"; // Success or error color
        toast.innerHTML = `${data.product_name} ${
          isSuccess ? "added to your cart!" : "is updated in your cart!"
        }`;

        message.appendChild(toast);

        $(toast).toast({ delay: 3000 });
        $(toast).toast("show");

        setTimeout(() => (toast.style.opacity = "1"), 10);
        setTimeout(() => (toast.style.opacity = "0"), 2900);

        // Play corresponding sound
        const audio = new Audio(
          isSuccess
            ? "https://res.cloudinary.com/dxfq3iotg/video/upload/v1557233524/success.mp3"
            : "https://res.cloudinary.com/dxfq3iotg/video/upload/v1557233294/info.mp3"
        );
        audio.play();
      })
      .catch((error) => {
        console.error("Error adding item to cart:", error);
      });
  });
  var buyButton = document.getElementById("buy_now");
  buyButton.addEventListener("click", (e) => {
    e.preventDefault();
    var product_slug = e.target.dataset.value;

    fetch(`http://127.0.0.1:8000/cart/buy_now`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ product_slug, newPrice, size, quantity }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (!data.success || data.success) {
          window.location.href = "http://127.0.0.1:8000/cart/cart";
        }
      });
  });
});
