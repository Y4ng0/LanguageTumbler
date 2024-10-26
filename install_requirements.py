import subprocess
import sys
import os


def install_requirements():
    requirements_file = 'requirements.txt'

    # Check if requirements.txt exists
    if not os.path.isfile(requirements_file):
        print(f"Error: {requirements_file} not found.")
        return

    # Read and install packages from requirements.txt
    try:
        print("Installing packages from requirements.txt...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
        print("All packages installed successfully.")
    except subprocess.CalledProcessError as e:
        print("Error occurred during package installation.")
        print(e)
    except Exception as e:
        print("An unexpected error occurred.")
        print(e)


if __name__ == "__main__":
    install_requirements()
