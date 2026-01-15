"""
Reset database and repopulate with current data.py
"""
import os
from app import app, db

# Delete existing database
db_path = 'trees.db'
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"Deleted {db_path}")

# Reinitialize
with app.app_context():
    db.create_all()
    print("Database recreated successfully!")
    
# Now run the init_db function from app
from app import init_db
init_db()

print("Database reset complete!")
