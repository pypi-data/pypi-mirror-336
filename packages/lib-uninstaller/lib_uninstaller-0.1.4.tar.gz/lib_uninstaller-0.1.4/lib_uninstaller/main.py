import pkg_resources
import subprocess

def list_installed_packages():
    """Fetch and return all installed Python libraries as a sorted list."""
    return sorted([pkg.key for pkg in pkg_resources.working_set])

def uninstall_packages():
    """Display installed packages, take user input, and uninstall selected ones."""
    installed_packages = list_installed_packages()

    print("Select the packages you want to uninstall (comma-separated):\n")
    for index, package in enumerate(installed_packages, start=1):
        print(f"{index}. {package}")

    selected_indices = input("\nEnter numbers of packages to uninstall (e.g., 1,3,5): ")
    selected_indices = [int(i.strip()) for i in selected_indices.split(",") if i.strip().isdigit()]

    selected_packages = [installed_packages[i - 1] for i in selected_indices if 0 < i <= len(installed_packages)]

    if selected_packages:
        print(f"\nYou have selected: {', '.join(selected_packages)}")
        confirm = input("Are you sure you want to uninstall these packages? (yes/no): ").strip().lower()
        
        if confirm == "yes":
            for package in selected_packages:
                subprocess.run(["pip", "uninstall", "-y", package])
            print("\nUninstallation complete.")
        else:
            print("\nUninstallation canceled.")
    else:
        print("\nNo valid packages selected.")

if __name__ == "__main__":
    uninstall_packages()
