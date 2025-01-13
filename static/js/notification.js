$(document).ready(function () {
  // Define options for the Toasty library
  var options = {
    autoClose: true,
    progressBar: true,
    enableSounds: true,
    sounds: {
      info: "https://res.cloudinary.com/dxfq3iotg/video/upload/v1557233294/info.mp3",
      success:
        "https://res.cloudinary.com/dxfq3iotg/video/upload/v1557233524/success.mp3",
      warning:
        "https://res.cloudinary.com/dxfq3iotg/video/upload/v1557233563/warning.mp3",
      error:
        "https://res.cloudinary.com/dxfq3iotg/video/upload/v1557233574/error.mp3",
    },
  };

  var toast = new Toasty(options);
  toast.configure(options);

  // Automatically display Django messages as toast notifications
  $(".toast").each(function () {
    var message = $(this).data("message");
    var level = $(this).data("level");

    switch (level) {
      case "success":
        toast.success(message);
        break;
      case "info":
        toast.info(message);
        break;
      case "warning":
        toast.warning(message);
        break;
      case "error":
        toast.error(message);
        break;
      default:
        toast.info(message);
    }
  });

  // Manually trigger toast notifications for buttons (if needed)

});
