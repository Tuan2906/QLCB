const paymentMethodSelect = document.getElementById("payment-method");

function thanhtoan(obj)
{
  const selectedValue = obj.value;
  const stripeScript = document.querySelector(".stripe-button-el");

  if (selectedValue === "Stripe") {
    stripeScript.style.display = "block";
    stripeScript.style.marginTop="300px";
    stripeScript.style.marginRight="183px";
    stripeScript.style.width="50%";
     stripeScript.setAttribute("src", "'https://checkout.stripe.com/checkout.js"); // Tải lại script nếu chưa tải
  }
  if(selectedValue === "TienMat"){
     var xacNhan = document.querySelector(".btnThanhToan");
     xacNhan.style.display = "block";

  }
};

document.addEventListener("DOMContentLoaded", () => {
  const stripeButton = document.querySelector(".stripe-button-el");
  stripeButton.style.display = "none";
});