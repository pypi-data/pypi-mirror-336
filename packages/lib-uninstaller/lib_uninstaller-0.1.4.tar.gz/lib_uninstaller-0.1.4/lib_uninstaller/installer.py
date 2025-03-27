import requests
import subprocess
import pkg_resources
import os
import socket
import warnings
from datetime import datetime
from thefuzz import process
from tqdm import tqdm  # For progress bar
from packaging import version  # For semantic version comparison

# Suppress unnecessary warnings
warnings.filterwarnings("ignore")

# List of popular libraries for fuzzy search
POPULAR_LIBRARIES = [
    "numpy", "pandas", "matplotlib", "seaborn", "scipy", "scikit-learn", "tensorflow", "keras", "torch",
    "flask", "django", "fastapi", "requests", "pytest", "opencv-python", "pillow", "plotly", "bokeh",
    "sympy", "statsmodels", "xgboost", "lightgbm", "catboost", "joblib", "multiprocessing", "threading",
    "asyncio", "celery", "sqlalchemy", "psycopg2", "mysql-connector-python", "sqlite3", "mongoengine",
    "pymongo", "redispy", "elasticsearch", "beautifulsoup4", "scrapy", "selenium", "lxml", "nltk",
    "spacy", "gensim", "transformers", "speechrecognition", "deepface", "face-recognition", "mediapipe",
    "tqdm", "rich", "loguru", "pydantic", "dataclasses", "marshmallow", "pyyaml", "json5", "argparse",
    "click", "fire", "pyinstaller", "cx_Freeze", "pyqt5", "tkinter", "kivy", "pygame", "arcade",
    "pytorch-lightning", "tensorboard", "onnx", "jax", "pymc3", "prophet", "pyod", "h2o", "mlflow",
    "dask", "modin", "vaex", "polars", "numba", "cython", "pybind11", "pycryptodome", "bcrypt",
    "cryptography", "scapy", "shodan", "paramiko", "fabric", "ansible", "boto3", "azure-sdk-for-python",
    "google-cloud-python", "pandas-profiling", "sweetviz", "great-expectations", "deap", "networkx",
    "igraph", "geopandas", "shapely", "folium", "pydeck", "pycaret", "auto-sklearn", "h2o-automl",
    "hyperopt", "optuna", "ray", "streamlit", "gradio", "dash", "panel"
]

def check_internet():
    """Check if there is an active internet connection."""
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

def install_package_from_pip(package_name, version=None):
    """Install a package using pip and capture the output for error handling."""
    command = ["pip", "install", package_name] if not version else ["pip", "install", f"{package_name}=={version}"]
    try:
        # Capture the output of the pip command
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def check_pypi_details(package_name):
    """Fetch package details from PyPI and sort versions correctly, ignoring invalid versions."""
    url = f"https://pypi.org/pypi/{package_name}/json"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            description = data.get("info", {}).get("summary", "No description available.")
            
            # Filter out invalid versions
            valid_versions = []
            for v in data.get("releases", {}).keys():
                try:
                    version.parse(v)  # Check if the version is valid
                    valid_versions.append(v)
                except version.InvalidVersion:
                    continue  # Skip invalid versions
            
            # Sort valid versions
            versions = sorted(valid_versions, key=version.parse, reverse=True)
            return True, description, versions
        return False, None, []
    except requests.RequestException:
        return False, None, []

def strong_fuzzy_search(query, package_dict):
    """Perform fuzzy search to find related packages."""
    results = process.extract(query, package_dict.keys(), limit=5)
    return [pkg for pkg, score in results if score > 60]

def check_installed_package(package_name):
    """Check if a package is installed and return its details."""
    try:
        package = pkg_resources.get_distribution(package_name)
        package_path = os.path.join(package.location, package.key)

        if os.path.exists(package_path):
            # Get the latest modification time of files in the package directory
            timestamps = [os.path.getmtime(os.path.join(package_path, f)) for f in os.listdir(package_path) if os.path.isfile(os.path.join(package_path, f))]
            install_datetime = datetime.fromtimestamp(max(timestamps)).strftime("%Y-%m-%d %H:%M:%S") if timestamps else "Unknown"

            # Calculate package size
            total_size = sum(os.path.getsize(os.path.join(package_path, f)) for f in os.listdir(package_path) if os.path.isfile(os.path.join(package_path, f)))
            total_size_mb = total_size / (1024 * 1024)  # Convert to MB

            # Count number of files
            file_count = len([f for f in os.listdir(package_path) if os.path.isfile(os.path.join(package_path, f))])

            return True, package.version, install_datetime, round(total_size_mb, 2), file_count
        else:
            return False, None, None, None, None
    except pkg_resources.DistributionNotFound:
        return False, None, None, None, None

def display_package_info(package_name, description, latest_version, installed, installed_version, install_datetime, package_size, file_count):
    """Display detailed information about a package."""
    print(f"\n📦 Package: {package_name}")
    print(f"📖 Description: {description}")
    print(f"🆕 Latest Version: {latest_version}")

    if installed:
        print(f"\n📌 Installed Version: {installed_version}")
        print(f"   Installed Date & Time: {install_datetime}")
        print(f"   Package Size: {package_size} MB")
        print(f"   Number of Files: {file_count}")
    else:
        print("\n⚠️ Package is not installed.")

def suggest_solution(error_message):
    """Analyze the error message and suggest potential solutions."""
    if "Could not find a version" in error_message or "No matching distribution found" in error_message:
        return (
            "🔧 Possible Solutions:\n"
            "1. Check if the package name is spelled correctly.\n"
            "2. Ensure your Python version is compatible with the package.\n"
            "3. Try upgrading pip: python -m pip install --upgrade pip.\n"
            "4. If the package is not on PyPI, it may be available on a different repository or require manual installation."
        )
    elif "Permission denied" in error_message or "access denied" in error_message.lower():
        return (
            "🔧 Possible Solutions:\n"
            "1. Try installing with elevated privileges: sudo pip install <package> (on Linux/Mac).\n"
            "2. Use the --user flag: pip install --user <package>.\n"
            "3. Check if your Python environment has write permissions."
        )
    elif "Failed building wheel" in error_message:
        return (
            "🔧 Possible Solutions:\n"
            "1. Ensure you have the required build tools installed (e.g., build-essential on Linux).\n"
            "2. Install the package with the --no-binary flag: pip install --no-binary <package>.\n"
            "3. Check if the package requires additional dependencies (e.g., libssl-dev for cryptography)."
        )
    elif "SSL: CERTIFICATE_VERIFY_FAILED" in error_message:
        return (
            "🔧 Possible Solutions:\n"
            "1. Update your system's CA certificates.\n"
            "2. Use the --trusted-host flag: pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org <package>.\n"
            "3. Check your network's SSL configuration."
        )
    else:
        return (
            "🔧 No specific solution found. Here are some general tips:\n"
            "1. Check your internet connection.\n"
            "2. Upgrade pip: python -m pip install --upgrade pip.\n"
            "3. Search online for the error message to find specific solutions."
        )

def install_package(package_name=None):
    if not check_internet():
        print("\n❌ No internet connection detected. Please check your connection and try again.")
        print("\nℹ️ No package installed. Exiting gracefully.")
        return  # End the program gracefully

    if package_name is None:
        query = input("Enter package name: ").strip()
    else:
        query = package_name

    found_on_pypi, package_description, available_versions = check_pypi_details(query)

    if not found_on_pypi:
        print(f"\n❌ No package found with the name '{query}'. Searching for related packages...")
        related_packages = strong_fuzzy_search(query, {pkg: None for pkg in POPULAR_LIBRARIES})

        if not related_packages:
            print("\nℹ️ No related packages found.")
            print("\nℹ️ No package installed. Exiting gracefully.")
            return  # End the program gracefully

        print("\n⚠️ Did you mean:")
        for i, pkg in enumerate(related_packages):
            found, description, _ = check_pypi_details(pkg)
            if found:
                print(f"{i+1}. {pkg} - {description}")
        choice = input("\nEnter the serial number of the package you want to install. Leave blank and press Enter to exit: ").strip()
        if choice == "" or not choice.isdigit() or not (1 <= int(choice) <= len(related_packages)):
            print("\nℹ️ Invalid selection.")
            print("\nℹ️ No package installed. Exiting gracefully.")
            return  # End the program gracefully
        query = related_packages[int(choice) - 1]
        print(f"\n🔍 Searching for '{query}'")
        found_on_pypi, package_description, available_versions = check_pypi_details(query)
        if not found_on_pypi:
            print(f"\n❌ '{query}' is also not available on PyPI.")
            print("\nℹ️ No package installed. Exiting gracefully.")
            return  # End the program gracefully

    installed, installed_version, install_datetime, package_size, file_count = check_installed_package(query)
    display_package_info(query, package_description, available_versions[0], installed, installed_version, install_datetime, package_size, file_count)

    if installed:
        # Compare versions using semantic versioning
        if version.parse(installed_version) < version.parse(available_versions[0]):
            choice = input("\nDo you want to upgrade to the latest version? (y/n): ").strip().lower()
            if choice == "y":
                print(f"\n⬆️ Upgrading '{query}' to version {available_versions[0]}...")
                success, output = install_package_from_pip(query, available_versions[0])
                if success:
                    print(f"\n✅ '{query}' has been updated to the latest version.")
                else:
                    print(f"\n❌ Failed to upgrade '{query}'.")
                    print(suggest_solution(output))
                    view_details = input("\nDo you want to view detailed error logs? (y/n): ").strip().lower()
                    if view_details == "y":
                        print("\nDetailed Error Logs:")
                        print(output)
        else:
            print(f"\n✅ '{query}' is already up to date (installed: {installed_version}, latest: {available_versions[0]}).")
    else:
        choice = input(f"\n⬇️ '{query}' is not installed. Do you want to install it? (y/n): ").strip().lower()
        if choice == "y":
            print(f"\n⬇️ Installing latest version of '{query}'...")
            success, output = install_package_from_pip(query, available_versions[0])
            if success:
                print(f"\n✅ '{query}' has been installed successfully.")
            else:
                print(f"\n❌ Failed to install '{query}'.")
                print(suggest_solution(output))
                view_details = input("\nDo you want to view detailed error logs? (y/n): ").strip().lower()
                if view_details == "y":
                    print("\nDetailed Error Logs:")
                    print(output)
        else:
            print("\nℹ️ No package installed. Exiting gracefully.")
