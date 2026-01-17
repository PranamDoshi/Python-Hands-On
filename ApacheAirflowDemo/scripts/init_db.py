#!/usr/bin/env python3
"""Script to initialize database tables."""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from db.connections.sql_db import sql_db

if __name__ == "__main__":
    print("Creating database tables...")
    sql_db.create_tables()
    print("Database tables created successfully!")
