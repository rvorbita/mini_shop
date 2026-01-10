from flask import Blueprint, session, redirect, url_for, render_template
from ..models import Product

cart_bp = Blueprint("cart", __name__)

@cart_bp.route("/add/<int:product_id>")
def add_to_cart(product_id):
    cart = session.get("cart", {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    session["cart"] = cart
    return redirect(url_for("cart.view_cart"))

@cart_bp.route("/cart")
def view_cart():
    cart = session.get("cart", {})
    items = []
    total = 0

    for pid, qty in cart.items():
        product = Product.query.get(int(pid))
        subtotal = product.price * qty
        total += subtotal
        items.append((product, qty, subtotal))

    return render_template("cart.html", items=items, total=total)

@cart_bp.route("/checkout")
def checkout():
    session.clear()
    return render_template("checkout.html")
