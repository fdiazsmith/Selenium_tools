#!/usr/bin/env bash


function check_venv_exists() {
    if [ -d "venv" ]; then
        echo "A Python virtual environment exists in the current directory."
        activate_venv
    else
        echo "A Python virtual environment does not exist in the current directory. please run 'sudo bash install.sh' first."
    fi
}

function activate_venv() {
    if [ -d "venv" ]; then
        echo "Activating the Python virtual environment..."
        source venv/bin/activate
        run_python3_main
    else
        echo "A Python virtual environment does not exist in the current directory."
    fi
}

function run_python3_main() {
    if [ -f "main.py" ]; then
        echo "Running main.py with Python 3..."
        python3 main.py
    else
        echo "main.py does not exist in the current directory."
    fi
}

check_venv_exists