#!/bin/bash
# Find My Tutor - Backend Setup
cd /home/kruthickesh/codebase/FT/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Initialize database
python init_db.py

echo "Backend setup complete!"
echo "Run 'source venv/bin/activate && uvicorn app.main:app --reload' to start the server"