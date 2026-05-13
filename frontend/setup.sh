#!/bin/bash
# Find My Tutor - Frontend Setup
cd /home/kruthickesh/codebase/FT/frontend

# Install dependencies
npm install

# Copy environment file
cp .env.local.example .env.local

echo "Frontend setup complete!"
echo "Run 'npm run dev' to start the development server"