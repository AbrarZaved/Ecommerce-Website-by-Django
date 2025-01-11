//Handling Authentication
var loginSubmit = document.getElementById("loginSubmit");
loginSubmit.addEventListener("click", (e) => {
  e.preventDefault();
  var loginPhone = document.getElementById("loginPhone").value;
  var loginPassword = document.getElementById("loginPassword").value;
  fetch("http://127.0.0.1:8000/auth/sign_in", {
    method: "POST",
    header: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ loginPhone, loginPassword }),
  }).then(() => {
    location.reload();
  });
});

var registerSubmit = document.getElementById("registerSubmit");
registerSubmit.addEventListener("click", (e) => {
  e.preventDefault();
  var registerPhone = document.getElementById("registerPhone").value;
  var registerPassword = document.getElementById("registerPassword").value;
  fetch("http://127.0.0.1:8000/auth/sign_up", {
    method: "POST",
    header: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ registerPhone, registerPassword }),
  }).then(() => {
    location.reload();
  });
});
