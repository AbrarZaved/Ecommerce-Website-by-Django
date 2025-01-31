document.addEventListener("DOMContentLoaded", function () {
  var message = document.getElementById("message");

  // Check if the user has logged in successfully
  if (localStorage.getItem("loggedIn") === "true") {
    notifications("Successfully Logged In", "loggedIn", "success");
  }
  if (localStorage.getItem("loggedIn") === "false") {
    notifications("Invalid Credentials", "loggedIn", "error");
    $("#exampleModalCenter").modal("show");
  }
  if (localStorage.getItem("regDone") === "false") {
    notifications("User Alerady Exists", "regDone", "error");
    $("#exampleModalCenter").modal("show");
  }
  if (localStorage.getItem("regDone") === "true") {
    notifications(
      "Registration Successful. Please complete your Profile",
      "regDone",
      "info"
    );
  }

  function notifications(topic, value, tag) {
    message.innerHTML += `
      <div data-message="${topic}" data-level="${tag}" class="toast">
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
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          localStorage.setItem("loggedIn", "true");
          location.reload();
        } else {
          localStorage.setItem("loggedIn", "false");
          location.reload();
        }
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
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          localStorage.setItem("regDone", "true");
          location.reload();
        } else {
          localStorage.setItem("regDone", "false");
          location.reload();
        }
      });
  });
});
