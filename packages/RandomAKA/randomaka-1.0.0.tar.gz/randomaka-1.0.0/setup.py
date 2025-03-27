from setuptools import setup, find_packages

setup(
    name="RandomAKA",  # Your package name
    version="1.0.0",  # Start with an initial version
    author="AnbuKumaran Arangaperumal",  # Your name
    author_email="anbuku12345@gmail.com",  # Your email
    description="A Python package for enhanced randomization functions",  # Short description
    long_description=open("README.md").read(),  # Import README.md for long description
    long_description_content_type="text/markdown",  # Markdown format
    url="https://github.com/anbukumaran1/RandomAKA",  # Link to your GitHub repo
    packages=find_packages(),  # Automatically find package folders
    license="MIT",  # Updated to SPDX format
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Specify supported Python versions
)
