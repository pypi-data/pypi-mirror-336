from setuptools import setup, find_packages

setup(
    name="bigbank",
    version="0.1.1",
    author="William Cunningham",
    author_email="mrcoolguy640@example.com",
    description="Really useless library that has no reason to exist !!!",
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