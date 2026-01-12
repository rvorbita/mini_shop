import os
import time
from werkzeug.security import generate_password_hash
from sqlalchemy import create_engine
from app import db
from app.models import User

# Configuration
DB_URI = os.environ.get("DATABASE_URL")
ADMIN_USER = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASS = os.environ.get("ADMIN_PASSWORD", "admin123")

# Wait for database
for i in range(20):
    try:
        engine = create_engine(DB_URI)
        conn = engine.connect()
        conn.close()
        print("Database is ready")
        break
    except Exception as e:
        print("Waiting for database...", e)
        time.sleep(5)
else:
    raise Exception("Database not ready")

# Create or update admin
admin = User.query.filter_by(username=ADMIN_USER).first()
hashed = generate_password_hash(ADMIN_PASS)

# Update or create admin user
if admin:
    admin.password = hashed
    print("Admin password updated")
else:
    # Create new admin user
    admin = User(
        username=ADMIN_USER,
        password=hashed,
        is_admin=True
    )
    db.session.add(admin)
    print("Admin created")

# Commit changes
db.session.commit()
print("Bootstrap admin finished")
