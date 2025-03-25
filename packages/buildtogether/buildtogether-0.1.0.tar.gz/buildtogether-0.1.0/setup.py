from setuptools import setup, find_packages
import os

# Read the contents of the README file
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="buildtogether",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask>=3.0.0",
        "SQLAlchemy>=2.0.20",
        "Flask-SQLAlchemy>=3.1.0",
        "Flask-Migrate>=4.0.0",
        "Flask-WTF>=1.1.0",
        "WTForms>=3.0.0",
        "marshmallow>=3.20.0",
        "python-dotenv>=1.0.0",
        "flask-cors>=4.0.0",
        "markdown>=3.7.0",
        "bleach>=6.2.0",
        "markupsafe>=3.0.0",
        "click>=8.0.0",     # Added for CLI functionality
        "psutil>=5.9.0",    # Added for process management
        "colorama>=0.4.6",  # Added for colored terminal output
    ],
    entry_points={
        "console_scripts": [
            "btg=buildtogether.cli:main",
        ],
    },
    python_requires=">=3.8",
    description="Build Together - Project Management Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Build Together Team",
    author_email="info@buildtogether.app",
    url="https://github.com/yourusername/buildtogether",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development",
    ],
)
