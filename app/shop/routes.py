from flask import Blueprint, render_template, session, redirect, url_for
from ..models import Product

shop_bp = Blueprint("shop", __name__)

@shop_bp.route("/")
def index():
    products = Product.query.all()
    return render_template("index.html", products=products)

@shop_bp.route("/product/<int:product_id>")
def product(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template("product.html", product=product)

@shop_bp.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    cart = session.get("cart", {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    session["cart"] = cart
    return redirect(url_for("shop.view_cart"))

@shop_bp.route("/cart")
def view_cart():
    cart = session.get("cart", {})
    items = []
    total = 0

    for pid, qty in cart.items():
        product = Product.query.get(int(pid))
        if product:
            subtotal = product.price * qty
            total += subtotal
            items.append((product, qty, subtotal))

    return render_template("cart.html", items=items, total=total)

@shop_bp.route("/checkout")
def checkout():
    session.clear()
    return render_template("checkout.html")
