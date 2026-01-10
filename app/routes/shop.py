from flask import Blueprint, render_template
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
