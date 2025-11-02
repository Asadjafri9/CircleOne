"""
Database migration script to add username and password_hash columns
Run this once to update your existing database
"""
from main import app, db
from sqlalchemy import text

with app.app_context():
    try:
        # Check if columns already exist
        result = db.session.execute(text("PRAGMA table_info(users)"))
        columns = [row[1] for row in result.fetchall()]
        
        # Add username column if it doesn't exist
        if 'username' not in columns:
            db.session.execute(text("ALTER TABLE users ADD COLUMN username VARCHAR(80)"))
            print("[OK] Added username column")
        else:
            print("[OK] username column already exists")
        
        # Add password_hash column if it doesn't exist
        if 'password_hash' not in columns:
            db.session.execute(text("ALTER TABLE users ADD COLUMN password_hash VARCHAR(255)"))
            print("[OK] Added password_hash column")
        else:
            print("[OK] password_hash column already exists")
        
        # Update oauth_provider default if needed
        if 'oauth_provider' in columns:
            # Check if any rows have NULL oauth_provider
            result = db.session.execute(text("SELECT COUNT(*) FROM users WHERE oauth_provider IS NULL"))
            null_count = result.scalar()
            if null_count > 0:
                db.session.execute(text("UPDATE users SET oauth_provider = 'local' WHERE oauth_provider IS NULL"))
                print(f"[OK] Updated {null_count} users with NULL oauth_provider")
        
        # Make email nullable (SQLite doesn't support MODIFY COLUMN, so this is informational)
        # For SQLite, we just note that existing constraints remain
        print("Note: Email column remains non-nullable due to SQLite limitations")
        print("New users created via signup can have NULL email")
        
        db.session.commit()
        print("\n[SUCCESS] Database migration completed successfully!")
        
    except Exception as e:
        db.session.rollback()
        print(f"[ERROR] Error during migration: {e}")
        print("\nIf migration fails, you may need to delete instance/app.db and recreate it.")
        print("This will delete all existing data!")

