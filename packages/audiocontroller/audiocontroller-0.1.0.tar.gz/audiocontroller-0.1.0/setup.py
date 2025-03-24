from setuptools import setup, find_packages

setup(
    name="audiocontroller",  # Name of your package
    version="0.1.0",  # Initial version of your package
    packages=find_packages(),  # Automatically detect and include package files
    install_requires=[],  # List dependencies if needed (e.g., ['pygame'])
    author="Harshitha",  # Replace with your name
    author_email="harshitha.atra1306@gmail.com",  # Replace with your email
    description="A simple Python library to control audio playback (play, pause, stop)",
    long_description=open("README.md").read(),  # Reads description from README.md
    long_description_content_type="text/markdown",  # Format of README.md
    url="https://github.com/Harshitha-atra/audio-control-lib.git",  # GitHub repo URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimum Python version requirement
)