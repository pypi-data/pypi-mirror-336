from setuptools import setup, find_packages

setup(
    name="namaztime",
    version="1.1.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'namaztime': ['timezone_city.json'],
    },
    description="Python package to get Islamic prayer times for any city using Aladhan API, for Muslims and Islam",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="raxmatullox",
    author_email="raxmatulllox@icloud.com",
    url="https://github.com/raxmatulloxswe/NamazTime-API",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.1",
    ],
)