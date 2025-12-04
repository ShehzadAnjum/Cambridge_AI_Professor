#!/bin/bash
# Test script to verify backend can be imported correctly

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$PROJECT_ROOT"

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
else
    echo "Error: Virtual environment not found."
    exit 1
fi

export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"
cd "$PROJECT_ROOT/webapp/backend"

echo "Testing backend imports..."
python3 -c "import app.main; print('✓ app.main imported successfully')"
python3 -c "from src.core_database.database import SessionLocal; print('✓ Database imports work')"
python3 -c "from src.a_star_workflow_orchestrator.orchestrator import LearningLoop; print('✓ LearningLoop imported successfully')"
echo ""
echo "All imports successful! Backend is ready to run."

