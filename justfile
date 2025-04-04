# Justfile for Battlestats
set windows-shell := ["C:\\Program Files\\Git\\bin\\sh.exe","-c"] # fix for windows

info:
    @echo "Battlestats is a tool for tracking and analyzing player statistics in games."
    @echo "It provides a web interface for viewing and managing player data."
    @echo "This Justfile contains various commands for building, testing, and running the project."
    @echo "Use 'just help' to see the available commands."

help:
    @echo "Available commands:"
    @echo "  run         - Run the application."
    @echo "  debug       - Run the application in debug mode."
    @echo "  install     - Install dependencies."
    @echo "  docker      - Builds and runs the application using the included Dockerfile and compose.yml. Also starts the database."
    @echo "  postgres    - Starts postgres database."
    @echo "  info        - Show information about the project."
    @echo "  help        - Show this help message."

install:
    @echo "Installing dependencies..."

    # Python
    @pip install -r requirements.txt
    @echo "Python dependencies installed."

    @echo "Dependencies installed."
run:
    @echo "Running the application..."
    @python3 main.py

debug:
    @echo "Running the application in debug mode..."
    @python3 main.py --debug    

docker:
    @echo "Building and running the application using Docker..."
    @docker compose up --build
    @echo "Docker containers started."

postgres:
    @echo "Starting PostgreSQL database..."
    @docker compose up -d postgres
    @echo "PostgreSQL database started."