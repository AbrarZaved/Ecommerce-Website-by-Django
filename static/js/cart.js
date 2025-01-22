document.addEventListener("DOMContentLoaded", function () {
  console.log("Hello");
  var coupon = document.getElementById("coupon");
  var discount = document.getElementById("discount");
  var total = document.getElementById("total");
  discount.style.display = "none";
  function fetch_values(quantity, productName, size, newPrice, discount_price) {
    fetch("update_cart", {
      method: "POST",
      header: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        quantity,
        productName,
        size,
        newPrice,
        discount_price,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          document.getElementById(
            "sub_total"
          ).textContent = `$ ${data.total_price}`;
          document.getElementById(
            "total"
          ).textContent = `$ ${data.total_price}`;
          if (data.total_price >= 1000) {
            coupon.disabled = false;
            coupon.placeholder = `Enter Coupon Code`;
          } else {
            coupon.disabled = true;
            coupon.placeholder = `Min spend $1000`;
          }
          document.getElementById("coupon").value = ``;
          discount.style.display = "none";
        }
      });
  }
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

  var quantity, size, productName, discount_price;

  // Event listener for quantity change
  document.querySelectorAll("[name=quantity]").forEach((item) => {
    item.addEventListener("change", (e) => {
      quantity = parseInt(e.target.value);
      productName = item.dataset.value;
      size = document.getElementById(`size-${productName}`).value;
      priceElement = document.getElementById(`price-${productName}`);
      price = parseInt(priceElement.getAttribute("data-price"));
      newPrice = calculatePrice(size, price);
      var discountElement = document.getElementById(`discount-${productName}`);
      discountElement.style.display = "none";
      if (quantity >= 3) {
        newPrice = newPrice * quantity - quantity * 100;
        if (newPrice >= 1000) {
          coupon.disabled = false;
          coupon.placeholder = `Enter Coupon Code`;
        } else {
          coupon.disabled = true;
          coupon.placeholder = `Min spend $1000`;
        }
        discount_price = quantity * 100;
        priceElement.textContent = `$ ${newPrice}`;
        discountElement.style.display = "block";
        discountElement.textContent = `$ ${100 * quantity}`;
      } else {
        discount_price = 0;
        newPrice = newPrice * quantity;

        priceElement.textContent = `$ ${newPrice}`;
      }

      fetch_values(quantity, productName, size, newPrice, discount_price);
    });
  });

  // Event listener for size change
  document.querySelectorAll("[name=size_select]").forEach((element) => {
    element.addEventListener("change", (e) => {
      size = e.target.value;
      productName = element.dataset.value;
      priceElement = document.getElementById(`price-${productName}`);
      quantity = parseInt(
        document.getElementById(`quantity-${productName}`).value
      );
      var discountElement = document.getElementById(`discount-${productName}`);
      discountElement.style.display = "none";
      price = parseInt(priceElement.getAttribute("data-price"));
      newPrice = calculatePrice(size, price);
      if (quantity >= 3) {
        newPrice = newPrice * quantity - quantity * 100;
        var discount_price = quantity * 100;

        priceElement.textContent = `$ ${newPrice}`;
        discountElement.style.display = "block";
        discountElement.textContent = `$ ${100 * quantity}`;
      } else {
        var discount_price = 0;
        newPrice = newPrice * quantity;
        priceElement.textContent = `$ ${newPrice}`;
      }
      fetch_values(quantity, productName, size, newPrice, discount_price);
    });
  });

  document.querySelector("[name='address']").addEventListener("change", (e) => {
    address_id = e.target.value;
    console.log(address_id);
    fetch(`http://127.0.0.1:8000/auth/shipping_address/${address_id}`)
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
      });
  });

  coupon.addEventListener("input", (e) => {
    coupon_name = e.target.value;
    fetch("coupon_handle", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ coupon_name }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.discount_price) {
          discount.style.display = "block";
          discount.textContent = `You got $${data.discount_price} discount`;
          total.textContent = `$ ${data.sub_total - data.discount_price}`;
        } else {
          discount.style.display = "none";
          total.textContent = `$ ${data.sub_total}`;
        }
      });
  });
});
