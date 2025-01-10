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
    categories.setAttribute("aria-expanded", "true");
  });

  dropdownMenu.addEventListener("mouseout", function () {
    categories.classList.remove("show");
    dropdownMenu.classList.remove("show");
    categories.setAttribute("aria-expanded", "false");
  });
}

