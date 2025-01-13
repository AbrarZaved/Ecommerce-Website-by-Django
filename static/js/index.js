document.addEventListener("DOMContentLoaded", function () {
  var message = document.getElementById("message");

  // Check if the user has logged in successfully
  if (localStorage.getItem("loggedIn") === "true") {
    notifications("Successfully Logged In", "loggedIn", "success");
  }
  if (localStorage.getItem("regDone") === "true") {
    notifications(
      "Registration Successfull. Please complete your Profile",
      "regDone",
      "info"
    );
  }
  function notifications(topic, value, tag) {
    message.innerHTML += `<div data-message="${topic}"
        data-level="${tag}" class="toast">
      </div>`;
    localStorage.removeItem(`${value}`); // Remove the flag after showing the message
  }

  // Handling Authentication
  var loginSubmit = document.getElementById("loginSubmit");
  loginSubmit.addEventListener("click", (e) => {
    e.preventDefault();
    var loginPhone = document.getElementById("loginPhone").value;
    var loginPassword = document.getElementById("loginPassword").value;
    fetch("http://127.0.0.1:8000/auth/sign_in", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ loginPhone, loginPassword }),
    }).then(() => {
      localStorage.setItem("loggedIn", "true"); // Set flag indicating successful login
      window.location.href = "/index"; // Redirect to the 'index' page
    });
  });

  // Register logic
  var registerSubmit = document.getElementById("registerSubmit");
  registerSubmit.addEventListener("click", (e) => {
    e.preventDefault();
    var registerPhone = document.getElementById("registerPhone").value;
    var registerPassword = document.getElementById("registerPassword").value;
    fetch("http://127.0.0.1:8000/auth/sign_up", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ registerPhone, registerPassword }),
    }).then(() => {
      localStorage.setItem("regDone", "true");
      window.location.href = "/index";
    });
  });

  document.querySelectorAll("#add_cart").forEach((element) => {
    element.addEventListener("click", (e) => {
      e.preventDefault();
      const cart_value = element.getAttribute("data-value");

      fetch("http://127.0.0.1:8000/cart/add_cart", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ cart_value }),
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
