#!/bin/bash

# Variables
CURRENT_DIR=$(pwd)

# Default values for arguments
DEFAULT_REQUIREMENTS_FILE="requirements.txt"
DEFAULT_DIRECTORY="$HOME/.python_venv"
VENV_NAME="Radar_python312"  # Leave this empty for the user to fill directly in the script
PYTHON_VERSION="3.12"

# Manually set this according to your operating system:
# - On Windows, use the full path to your Python interpreter (e.g., "C:\Path\To\Python\python.exe").
# - On Linux or WSL, you can use "python3.12" or any other Python version you have installed.
PYTHON_INTERPRETER_UBUNTU="python3.12"
PYTHON_INTERPRETER_WINDOWS="C:\Users\Max\AppData\Local\Programs\Python\Python312\python.exe"

### Check if OS is Windows (Linux by exclusion principle)
# Assert it isn't MacOS
if [ "$(uname)" == "Darwin" ]; then
    echo "Error: MacOS is not supported. Please run this script on a Windows or Linux machine."
    exit 1
fi
# Is it Windows, else it must be Linux
if [ -n "$WINDIR" ]; then
    # Windows
    echo "OS is Windows"
    WINDOWS_FLAG="1"
    LINUX_FLAG="0"
    PYTHON_INTERPRETER="$PYTHON_INTERPRETER_WINDOWS"
else
    # Linux
    echo "OS is Linux (by exclusion principle)"
    WINDOWS_FLAG="0"
    LINUX_FLAG="1"
    PYTHON_INTERPRETER="$PYTHON_INTERPRETER_UBUNTU"
fi

# Function to check if necessary variables are set
check_variables() {
    if [ -z "$VENV_NAME" ]; then
        echo "Error: VENV_NAME is not set. Please set it directly in the script before running."
        exit 1
    fi

    if [ -z "$PYTHON_INTERPRETER" ]; then
        echo "Error: PYTHON_INTERPRETER is not set. Please set it directly in the script before running."
        exit 1
    fi

    # Check if the specified Python interpreter exists and is executable
    if ! command -v "$PYTHON_INTERPRETER" &> /dev/null; then
        echo "Error: Python interpreter '$PYTHON_INTERPRETER' not found or is not executable."
        exit 1
    fi

    # Check if the Python interpreter is of the correct version
    ACTUAL_PYTHON_VERSION=$("$PYTHON_INTERPRETER" --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
    EXPECTED_PYTHON_VERSION_MAJOR_MINOR=$(echo "$PYTHON_VERSION" | cut -d'.' -f1,2)

    if [ "$ACTUAL_PYTHON_VERSION" != "$EXPECTED_PYTHON_VERSION_MAJOR_MINOR" ]; then
        echo "Error: The Python interpreter '$PYTHON_INTERPRETER' is not of the expected version."
        echo "Expected: Python $EXPECTED_PYTHON_VERSION_MAJOR_MINOR, but found: Python $ACTUAL_PYTHON_VERSION"
        exit 1
    fi
}

# Parse arguments
usage() {
    echo "Usage: $0 [options]"
    echo "Options:"
    echo "  --requirements-file=PATH  Path to the requirements.txt file (default: $DEFAULT_REQUIREMENTS_FILE)"
    echo "  --directory=PATH          Directory where the virtual environment should be created (default: $DEFAULT_DIRECTORY)"
    echo "  --show-packages           Show installed packages after setup"
    echo "  --update                  Update the virtual environment with new packages and updates"
    echo "  --help                    Display this help message"
    exit 0
}

# Initialize variables with default values
REQUIREMENTS_FILE="$DEFAULT_REQUIREMENTS_FILE"
DIRECTORY="$DEFAULT_DIRECTORY"
SHOW_PACKAGES_FLAG=0
UPDATE_FLAG=0

# Parse arguments passed to the script
for i in "$@"; do
    case $i in
        --requirements-file=*)
        REQUIREMENTS_FILE="${i#*=}"
        shift
        ;;
        --directory=*)
        DIRECTORY="${i#*=}"
        shift
        ;;
        --show-packages)
        SHOW_PACKAGES_FLAG=1
        shift
        ;;
        --update)
        UPDATE_FLAG=1
        shift
        ;;
        --help)
        usage
        ;;
        *)
        # unknown option
        echo "Unknown option: $i"
        usage
        ;;
    esac
done

# Check if all necessary variables are correctly set
check_variables

# Check if the directory exists, if not, create it
if [ ! -d "$DIRECTORY" ]; then
    mkdir -p "$DIRECTORY"
fi

# Activate virtual environment if it exists, otherwise create it
ACTIVATION_COMMAND="$DIRECTORY/$VENV_NAME/bin/activate"
VENV_PYTHON="$DIRECTORY/$VENV_NAME/bin/python"

if [ -d "$DIRECTORY/$VENV_NAME" ]; then
    echo "Activating existing virtual environment $VENV_NAME"
    source "$ACTIVATION_COMMAND"
else
    echo "Creating virtual environment $VENV_NAME"
    $PYTHON_INTERPRETER -m venv "$DIRECTORY/$VENV_NAME"
    source "$ACTIVATION_COMMAND"
fi

# Install or update packages from requirements.txt
if [ -f "$REQUIREMENTS_FILE" ]; then
    if [ "$UPDATE_FLAG" -eq 1 ]; then
        echo "Updating packages from $REQUIREMENTS_FILE"
        "$VENV_PYTHON" -m pip install --upgrade -r "$REQUIREMENTS_FILE"
    else
        echo "Installing packages from $REQUIREMENTS_FILE"
        "$VENV_PYTHON" -m pip install -r "$REQUIREMENTS_FILE"
    fi
else 
    echo "No requirements.txt file found at $REQUIREMENTS_FILE. Skipping package installation."
fi

# Print command to activate the virtual environment
echo "To activate the virtual environment, run:"
echo "source \"$ACTIVATION_COMMAND\""
echo "To deactivate run the command: deactivate"

# Optionally display all installed packages in the virtual environment
if [ "$SHOW_PACKAGES_FLAG" -eq 1 ]; then
    echo "Installed packages in the virtual environment:"
    "$VENV_PYTHON" -m pip list
fi

echo " --- Virtual environment setup complete ---"