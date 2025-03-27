from .main import uninstall_packages, list_installed_packages
from .upgrader import upgrade_packages_gui
from .installer import install_package
"""
lib-uninstaller: A Python package to manage installed libraries with options to uninstall and upgrade packages.

This package provides a command-line and GUI-based approach to:
1. **List Installed Packages** - View all installed Python libraries.
2. **Uninstall Selected Packages** - Choose and uninstall multiple packages interactively.
3. **Upgrade Outdated Packages** - Identify and upgrade outdated libraries using a GUI.

Modules:
---------
- `lib_uninstaller.main`:
    - `list_installed_packages()`: Returns a list of installed Python packages.
    - `uninstall_packages()`: Interactive CLI tool for uninstalling selected packages.

- `lib_uninstaller.upgrader`:
    - `get_outdated_packages()`: Fetches a list of outdated packages.
    - `upgrade_selected(package_listbox, root, upgrade_button)`: Handles package upgrades in the GUI.
    - `upgrade_packages_gui()`: Opens a GUI to upgrade outdated packages.

Usage:
---------
1. **Uninstall Packages (CLI)**
    ```python
    import lib_uninstaller.main as uninstaller
    uninstaller.uninstall_packages()
    ```

2. **Upgrade Packages (GUI)**
    ```python
    import lib_uninstaller.upgrader as upgrader
    upgrader.upgrade_packages_gui()
    ```

Author: [Areeb Khan]  
License: MIT  
Outlook: [khan.areeb002@outlook.com]  
"""
