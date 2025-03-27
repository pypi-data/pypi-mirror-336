# setup.py

from setuptools import setup, find_packages

setup(
    name="dynamic-query-builder",  # Package name (you can change this)
    version="0.1.0",  # Initial version
    packages=find_packages(),  # Automatically find all packages
    install_requires=[  # Required dependencies
        "sqlalchemy>=1.4",
        "fastapi>=0.68",
        "asyncpg",
    ],
    author="Md Anisur Rahman",
    author_email="anisurrahman14046@gmail.com",
    description="A dynamic query builder with filtering, pagination, and sorting for SQLAlchemy models.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    # url="https://github.com/yourusername/dynamic-query-builder",  # Change this to your repo URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Choose the license you want
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
