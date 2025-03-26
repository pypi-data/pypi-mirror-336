from setuptools import setup, find_packages

setup(
    name="authentication-app-psgrl",  # Unique name for your package
    version="0.1.4",  # Initial version
    author="Mohd Ravi",
    author_email="mohd.ravi@cloudanalogy.com",
    description="A Python package for JWT-based authentication",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/raviforcebolt/jwt_authenticator.git",  # Your project repository
    packages=find_packages(),
    install_requires=[
        "PyJWT>=2.7.0,<3.0.0",         # PyJWT version 2.7.0 or above, but below 3.0.0
        "psycopg2-binary>=2.9.0,<3.0.0",       # PostgreSQL adapter for Python
        "azure-functions>=1.7.0,<2.0.0",  # Azure Functions SDK, specifying stable version
        "pytest>=7.0.0,<8.0.0"         # Pytest version 7.0.0 or above, but below 8.0.0
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
