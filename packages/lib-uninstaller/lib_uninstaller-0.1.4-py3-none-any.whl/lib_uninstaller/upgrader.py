import subprocess
import sys
import json
import tkinter as tk
from tkinter import messagebox

def get_outdated_packages():
    """Fetch a list of outdated packages using pip in JSON format."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list", "--outdated", "--format=json"],
            capture_output=True, text=True, check=True
        )
        outdated_packages = json.loads(result.stdout)
        return [pkg["name"] for pkg in outdated_packages]
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to fetch outdated packages:\n{e}")
        return []

def upgrade_selected(package_listbox, root, upgrade_button):
    """Upgrade selected packages."""
    selected = [package_listbox.get(i) for i in package_listbox.curselection()]
    if not selected:
        messagebox.showinfo("No Selection", "Please select at least one package to upgrade.")
        return

    upgrade_button.config(state=tk.DISABLED)  # Disable button during update
    for package in selected:
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", package])

    messagebox.showinfo("Upgrade Complete", "Selected packages have been upgraded.")
    root.destroy()  # Close the window after upgrade

def upgrade_packages_gui():
    """Open a GUI to upgrade selected outdated Python packages."""
    root = tk.Tk()
    root.title("Upgrade Python Packages")
    root.geometry("400x400")

    packages = get_outdated_packages()

    if not packages:
        messagebox.showinfo("Up to Date", "All packages are already up to date.")
        root.destroy()
        return

    tk.Label(root, text="Select packages to upgrade:", font=("Arial", 12)).pack(pady=10)

    package_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, width=50, height=15)
    for package in packages:
        package_listbox.insert(tk.END, package)
    package_listbox.pack(pady=10)

    upgrade_button = tk.Button(root, text="Upgrade Selected", command=lambda: upgrade_selected(package_listbox, root, upgrade_button))
    upgrade_button.pack(pady=10)

    root.mainloop()
