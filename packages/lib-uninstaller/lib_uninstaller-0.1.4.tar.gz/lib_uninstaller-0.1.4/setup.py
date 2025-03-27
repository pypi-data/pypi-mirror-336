from setuptools import setup, find_packages

setup(
    name="lib-uninstaller",
    version="0.1.4",
    author="Your Name",
    author_email="your.email@example.com",
    description="A simple Python package to uninstall selected libraries via CLI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/lib-uninstaller",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "lib-uninstaller=lib_uninstaller.main:uninstall_packages",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
