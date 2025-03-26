"""Setup configuration for Cacao."""
from setuptools import setup, find_packages
from pathlib import Path

# Read version from file
version_file = Path("VERSION")
if version_file.exists():
    version = version_file.read_text().strip()
else:
    version = "1.0.0"

# Read README for long description
readme = Path("README.md")
if readme.exists():
    long_description = readme.read_text()
else:
    long_description = "A flexible documentation generator with plugin support for Python applications."

# Read requirements
requirements = Path("requirements.txt")
if requirements.exists():
    install_requires = [
        line.strip()
        for line in requirements.read_text().splitlines()
        if line.strip() and not line.startswith("#")
    ]
else:
    install_requires = [
        "flask>=2.0.0",
        "jinja2>=3.0.0",
        "pyyaml>=6.0.0",
        "markdown2>=2.4.0",
        "beautifulsoup4>=4.9.0",
        "typing-extensions>=4.0.0",
        "python-dotenv>=0.19.0"
    ]

setup(
    name="cacao",
    version=version,
    description="A flexible documentation generator with plugin support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Juan Denis",
    author_email="juan@vene.co",
    url="https://github.com/jhd3197/CacaoDocs",
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Documentation",
        "Topic :: Software Development :: Documentation",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "cacao=cacaodocs.cli:main",
        ],
    },
    package_data={
        "cacao": [
            "templates/*.html",
            "templates/assets/css/*.css",
            "templates/assets/js/*.js",
            "templates/assets/img/*",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/yourusername/cacao/issues",
        "Source": "https://github.com/yourusername/cacao",
        "Documentation": "https://github.com/yourusername/cacao#readme",
    },
)
