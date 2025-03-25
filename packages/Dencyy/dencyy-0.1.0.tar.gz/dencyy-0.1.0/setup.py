from setuptools import setup, find_packages

# Read the contents of README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="Dencyy",
    version="0.1.0",
    author="PRIMUS",
    author_email="alokpal280@gmail.com",
    description="Generate requirements.txt by scanning Python imports",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/11PRIMUS/Dency",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/req-generator/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
    ],
    entry_points={
        "console_scripts": [
            "req-generator=Dencyy.cli:main",
        ],
    },
)