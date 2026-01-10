import os
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, abort
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from ..models import Product
from ..extensions import db
from functools import wraps

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# Decorator to allow only admins
def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return func(*args, **kwargs)
    return wrapper

# Allowed image extensions
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in current_app.config["ALLOWED_EXTENSIONS"]

# -----------------------------
# Admin Dashboard - List Products
# -----------------------------
@admin_bp.route("/dashboard")
@login_required
@admin_required
def dashboard():
    products = Product.query.all()
    return render_template("admin/dashboard.html", products=products)

# -----------------------------
# Add Product
# -----------------------------
@admin_bp.route("/add", methods=["GET", "POST"])
@login_required
@admin_required
def add_product():
    if request.method == "POST":
        # Get form data safely
        name = request.form.get("name")
        price = request.form.get("price")
        description = request.form.get("description")

        if not name or not price:
            flash("Product name and price are required.", "danger")
            return redirect(url_for("admin.add_product"))

        # Handle image upload
        file = request.files.get("image")
        filename = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))

        # Create and save product
        p = Product(name=name, price=float(price), description=description, image=filename)
        db.session.add(p)
        db.session.commit()
        flash("Product added successfully.", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/add_product.html")

# -----------------------------
# Edit Product
# -----------------------------
@admin_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_product(id):
    product = Product.query.get_or_404(id)

    if request.method == "POST":
        # Use .get() to avoid KeyError
        name = request.form.get("name")
        price = request.form.get("price")
        description = request.form.get("description")

        if name:
            product.name = name
        if price:
            product.price = float(price)
        product.description = description

        # Handle image upload
        file = request.files.get("image")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
            product.image = filename

        db.session.commit()
        flash("Product updated successfully.", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/edit_product.html", product=product)

# -----------------------------
# Delete Product
# -----------------------------
@admin_bp.route("/delete/<int:id>")
@login_required
@admin_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted successfully.", "info")
    return redirect(url_for("admin.dashboard"))
