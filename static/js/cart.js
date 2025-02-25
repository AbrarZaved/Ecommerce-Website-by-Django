document.addEventListener("DOMContentLoaded", function () {
  const { jsPDF } = window.jspdf;
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
        if (newPrice >= 1000) {
          coupon.disabled = false;
          coupon.placeholder = `Enter Coupon Code`;
        } else {
          coupon.disabled = true;
          coupon.placeholder = `Min spend $1000`;
        }
        priceElement.textContent = `$ ${newPrice * quantity - quantity * 100}`;
        discountElement.style.display = "block";
        discountElement.textContent = `$ ${100 * quantity}`;
      } else {
        discount_price = 0;
        priceElement.textContent = `$ ${newPrice * quantity}`;
      }
      console.log(newPrice, quantity, productName, size, discount_price);
      fetch_values(quantity, productName, size, newPrice, discount_price);
    });
  });
  document.querySelectorAll("[name=size_select]").forEach((item) => {
    item.addEventListener("change", (e) => {
      productName = item.dataset.value;
      quantity = parseInt(document.getElementById(`quantity-${productName}`).value);
      size = document.getElementById(`size-${productName}`).value;
      priceElement = document.getElementById(`price-${productName}`);
      price = parseInt(priceElement.getAttribute("data-price"));
      newPrice = calculatePrice(size, price);
      var discountElement = document.getElementById(`discount-${productName}`);
      discountElement.style.display = "none";
      if (quantity >= 3) {
        if (newPrice >= 1000) {
          coupon.disabled = false;
          coupon.placeholder = `Enter Coupon Code`;
        } else {
          coupon.disabled = true;
          coupon.placeholder = `Min spend $1000`;
        }
        priceElement.textContent = `$ ${newPrice * quantity - quantity * 100}`;
        discountElement.style.display = "block";
        discountElement.textContent = `$ ${100 * quantity}`;
      } else {
        discount_price = 0;
        priceElement.textContent = `$ ${newPrice * quantity}`;
      }
      console.log(newPrice, quantity, productName, size, discount_price);
      fetch_values(quantity, productName, size, newPrice, discount_price);
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
        console.log(data);
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

  // Event listener for size change
  document.getElementById("checkout").addEventListener("click", async () => {
    // Show loading modal immediately
    $("#cartLoading").modal("show");

    // Create a delay promise of 3.5 seconds
    const delay = new Promise((resolve) => setTimeout(resolve, 3500));

    try {
      // Fetch checkout data asynchronously
      const fetchData = fetch("checkout").then((res) => res.json());

      // Wait for both fetch and delay to finish
      const data = await Promise.all([fetchData, delay]).then(([res]) => res);

      // Hide the loading modal after 3.5 seconds
      $("#cartLoading").modal("hide");

      const pdf = new jsPDF();

      // Business Information
      pdf.setFontSize(16);
      pdf.text("Golpo Ghor", 10, 10);
      pdf.setFontSize(10);
      pdf.text("Kadiganj, Bornali, Rajshahi", 10, 15);
      pdf.text("Phone: 01728150570 | Email: golpoghor@gmail.com", 10, 20);

      // Invoice Details
      pdf.setFontSize(12);
      pdf.text(`Invoice #: ${new Date().getTime()}`, 140, 10);
      pdf.text(`Date: ${new Date().toLocaleDateString()}`, 140, 20);
      pdf.line(10, 75, 200, 75);

      // Client Details Header
      pdf.setFontSize(12);
      pdf.text("Invoice issued to:", 10, 40);
      pdf.setFontSize(10);

      // Client Information
      const client = data[data.length - 1];
      pdf.text(`Name: ${client[3] || "Unknown"}`, 10, 45);
      pdf.text(`Address: ${client[6] || "N/A"}`, 10, 50);
      pdf.text(`Email: ${client[5] || "N/A"} | Phone: ${client[4]}`, 10, 55);

      // Add a line under Client Information for separation
      pdf.line(10, 75, 200, 75);

      // Table Header
      const tableColumns = [
        "#",
        "Product",
        "Size",
        "Quantity",
        "Price",
        "Discount Price",
      ];
      const tableRows = data
        .slice(0, -1)
        .map((item, index) => [
          index + 1,
          item[0] || "Unknown Title",
          item[1] || "No Size Info",
          item[2] || 0,
          `$${item[3] + item[4] || 0}`,
          `$${item[4] || 0}`,
        ]);

      // AutoTable
      pdf.autoTable({
        head: [tableColumns],
        body: tableRows,
        startY: 80,
        theme: "striped",
        headStyles: {
          fontSize: 12,
          halign: "center",
          fillColor: [33, 33, 33],
        },
        bodyStyles: { fontSize: 10, halign: "center" },
        columnStyles: {
          0: { halign: "center" },
          4: { halign: "center" },
          5: { halign: "center" },
        },
      });

      // Add Totals Below the Table
      const finalY = pdf.autoTable.previous.finalY + 10;
      pdf.setFontSize(12);
      pdf.setTextColor(100);
      pdf.text(`Subtotal: `, 140, finalY, { align: "right" });
      pdf.setFont("helvetica", "bold");
      pdf.text(`$${(client[1] + client[0]).toFixed(2)}`, 180, finalY, {
        align: "right",
      });

      if (client[2] != null) {
        pdf.setFont("helvetica", "normal");
        pdf.text(`Coupon: `, 140, finalY + 5, { align: "right" });
        pdf.setFont("helvetica", "bold");
        pdf.text(`${client[2]}`, 180, finalY + 5, { align: "right" });
        pdf.setFont("helvetica", "normal");
        pdf.text(`Discount: `, 140, finalY + 10, { align: "right" });
        pdf.setFont("helvetica", "bold");
        pdf.text(`$${client[0].toFixed(2)}`, 180, finalY + 10, {
          align: "right",
        });
        pdf.setFont("helvetica", "normal");
        pdf.text(`Total: `, 140, finalY + 15, { align: "right" });
        pdf.setFont("helvetica", "bold");
        pdf.text(`$${client[1].toFixed(2)}`, 180, finalY + 15, {
          align: "right",
        });
      } else {
        pdf.setFont("helvetica", "normal");
        pdf.text(`Discount: `, 140, finalY + 5, { align: "right" });
        pdf.setFont("helvetica", "bold");
        pdf.text(`$${client[0].toFixed(2)}`, 180, finalY + 5, {
          align: "right",
        });
        pdf.setFont("helvetica", "normal");
        pdf.text(`Total: `, 140, finalY + 10, { align: "right" });
        pdf.setFont("helvetica", "bold");
        pdf.text(`$${client[1].toFixed(2)}`, 180, finalY + 10, {
          align: "right",
        });
      }

      // Footer note
      pdf.setFontSize(10);
      pdf.setTextColor(100);
      pdf.text(
        "Note: This is a system-generated invoice and does not require a signature.",
        10,
        finalY + 45
      );

      // Footer line
      pdf.line(10, finalY + 40, 200, finalY + 40);

      // Save PDF
      pdf.save(`invoice_of_${client[3] || "Unknown"}.pdf`);
      localStorage.setItem("cart", true);

      window.location.href = "http://127.0.0.1:8000/index";
    } catch (err) {
      console.error(err);
      $("#cartLoading").modal("hide");
    }
  });
});
