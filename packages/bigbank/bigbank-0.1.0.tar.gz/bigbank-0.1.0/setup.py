from setuptools import setup, find_packages

setup(
    name="bigbank",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A simple banking simulation package with cooldown mechanics.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/developer-cunningham/bigbank",
    packages=find_packages(),
    include_package_data=True,
    package_data={"bigbank": ["bigbank_save.json"]},  # Ensures JSON file is included
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)