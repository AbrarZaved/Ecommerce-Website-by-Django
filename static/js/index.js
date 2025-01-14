document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll("#add_cart").forEach((element) => {
    element.addEventListener("click", (e) => {
      e.preventDefault();
      const cart_value = element.getAttribute("data-value");

      fetch(`http://127.0.0.1:8000/cart/add_cart/${cart_value}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((res) => res.json())
        .then((data) => {
          const message = document.getElementById("message");
          message.innerHTML = ""; // Clear previous toasts

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
          toast.style.backgroundColor = isSuccess ? "#007bff" : "#790004"; // Success or error color
          toast.innerHTML = `${data.product_name} ${
            isSuccess ? "added to your cart!" : "is already in your cart!"
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
              : "https://res.cloudinary.com/dxfq3iotg/video/upload/v1557233574/error.mp3"
          );
          audio.play();
        })
        .catch((error) => {
          console.error("Error adding item to cart:", error);
        });
    });
  });
});
