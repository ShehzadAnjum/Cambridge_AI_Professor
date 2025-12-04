#!/bin/bash
# Script to start the FastAPI backend server

# Get the project root directory (one level up from webapp directory)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# Script is in webapp/, so project root is one level up
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Change to project root
cd "$PROJECT_ROOT"

# Activate virtual environment (check if already activated first)
if [ -z "$VIRTUAL_ENV" ]; then
    if [ -f "$PROJECT_ROOT/venv/bin/activate" ]; then
        source "$PROJECT_ROOT/venv/bin/activate"
    elif [ -f "$PROJECT_ROOT/.venv/bin/activate" ]; then
        source "$PROJECT_ROOT/.venv/bin/activate"
    else
        echo "Error: Virtual environment not found at $PROJECT_ROOT/venv or $PROJECT_ROOT/.venv"
        echo "Please create a virtual environment first."
        exit 1
    fi
else
    echo "Using already activated virtual environment: $VIRTUAL_ENV"
fi

# Set PYTHONPATH to project root so src imports work (export for subprocesses)
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"

# Get the venv's Python and uvicorn paths
if [ -n "$VIRTUAL_ENV" ]; then
    VENV_BIN="$VIRTUAL_ENV/bin"
else
    if [ -d "$PROJECT_ROOT/.venv/bin" ]; then
        VENV_BIN="$PROJECT_ROOT/.venv/bin"
    elif [ -d "$PROJECT_ROOT/venv/bin" ]; then
        VENV_BIN="$PROJECT_ROOT/venv/bin"
    else
        echo "Error: Could not find virtual environment"
        exit 1
    fi
fi

UVICORN_BIN="$VENV_BIN/uvicorn"

echo "Starting FastAPI backend server..."
echo "Backend will be available at: http://127.0.0.1:8000"
echo "API documentation at: http://127.0.0.1:8000/docs"
echo "Project root: $PROJECT_ROOT"
echo "Using uvicorn from: $UVICORN_BIN"
echo "PYTHONPATH: $PYTHONPATH"
echo ""

# Change to backend directory where app module is located
cd "$PROJECT_ROOT/webapp/backend"

# Run uvicorn using the venv's uvicorn explicitly
# This ensures the subprocess uses the correct Python environment
exec "$UVICORN_BIN" app.main:app --reload --host 127.0.0.1 --port 8000

