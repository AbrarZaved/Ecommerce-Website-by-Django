console.log("Hello");

document.addEventListener("DOMContentLoaded", hover_effect);

// Adding Hover Effect to the Dropdown Menu
function hover_effect() {
  var categories = document.querySelector("[name='dropdown']");
  var dropdownMenu = document.querySelector(".dropdown-menu");

  categories.addEventListener("mouseover", function () {
    console.log("hovered");
    categories.classList.add("show");
    dropdownMenu.classList.add("show");
    categories.setAttribute("aria-expanded", "true");
  });

  categories.addEventListener("mouseout", function () {
    categories.classList.remove("show");
    dropdownMenu.classList.remove("show");
    categories.setAttribute("aria-expanded", "false");
  });

  dropdownMenu.addEventListener("mouseover", function () {
    categories.classList.add("show");
    dropdownMenu.classList.add("show");
    categories.setAttribute("aria-expanded", "false");
  });

  dropdownMenu.addEventListener("mouseout", function () {
    categories.classList.remove("show");
    dropdownMenu.classList.remove("show");
    categories.setAttribute("aria-expanded", "true");
  });
}

//Handling Authentication

var loginSubmit = document.getElementById("loginSubmit");
loginSubmit.addEventListener("click", (e) => {
  e.preventDefault();
  var loginPhone = document.getElementById("loginPhone").value;
  var loginPassword = document.getElementById("loginPassword").value;
  fetch("signin", {
    method: "POST",
    header: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ loginPhone, loginPassword }),
  });
});
