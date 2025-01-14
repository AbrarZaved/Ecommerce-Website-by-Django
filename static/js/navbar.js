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

   
});
