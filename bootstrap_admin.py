# bootstrap_admin.py
import os
from app import create_app
from app.extensions import db
from app.models import User

# Load environment variables
ADMIN_USERNAME = os.getenv("FIRST_ADMIN_USER", "admin")
ADMIN_PASSWORD = os.getenv("FIRST_ADMIN_PASSWORD", "admin123")

app = create_app()

with app.app_context():
    # Check if any admin already exists
    existing_admin = User.query.filter_by(is_admin=True).first()
    if existing_admin:
        print(f"Admin user already exists: {existing_admin.username}")
    else:
        # Create first admin
        admin_user = User(username=ADMIN_USERNAME, is_admin=True)
        admin_user.set_password(ADMIN_PASSWORD)
        db.session.add(admin_user)
        db.session.commit()
        print(f"First admin created: {ADMIN_USERNAME}")
