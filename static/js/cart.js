$(document).ready(() => {
  const updateCart = async (id, action, quantity) => {
    try {
      const res = await axios.post(
        "/store/update-item/",
        {
          productId: id,
          action,
        },
        {
          headers: {
            "X-CSRFToken": csrftoken,
          },
        }
      );
      $("#cart-number").text(res.data.cart);
      const event = new CustomEvent("cart_update", { time: new Date() });
      document.dispatchEvent(event);
    } catch (error) {
      console.log(error);
    }
  };

  const addCookieItem = (productId, action, url) => {
    console.log(cart);

    if (cart[productId] == undefined) {
      cart[productId] = { quantity: 1 };
    } else {
      const itemQ = cart[productId]["quantity"];
      cart[productId]["quantity"] = 1;
    }
    document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/";
    location.href = url;
  };
  $(".update-cart").click(async (e) => {
    const id = e.target.getAttribute("data-pk");
    const action = e.target.getAttribute("data-action");
    const url = e.target.getAttribute("href");

    if (user == "AnonymousUser") {
      e.preventDefault();
      console.log("User anonymous");
      addCookieItem(id, action, url);
    } else {
    }
  });
});
