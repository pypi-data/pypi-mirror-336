from setuptools import setup, find_packages

setup(
    name="whitebit_connector",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",  # Ensure all necessary dependencies are included
        "hummingbot"  # Ensure compatibility with Hummingbot
    ],
    include_package_data=True,
    description="Custom Whitebit connector for Hummingbot",
    author="GushALKDev",
    author_email="",
    url="https://github.com/GushALKDev/whitebit_connector",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)