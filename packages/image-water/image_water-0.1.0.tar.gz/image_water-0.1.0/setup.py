from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="image_water",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "Pillow"
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A simple Python package for adding watermarks to images.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/image_water",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
