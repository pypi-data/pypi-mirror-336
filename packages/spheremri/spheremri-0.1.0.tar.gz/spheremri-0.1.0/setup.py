from setuptools import setup, find_packages
import os

# Create a basic README if it doesn't exist
if not os.path.exists("README.md"):
    with open("README.md", "w", encoding="utf-8") as f:
        f.write("# sphereMRI\n\nA tool for MR image motion artifact quantification using deep learning.")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="spheremri",
    version="0.1.0",
    author="Jinghan Li",
    author_email="jinghang.li@pitt.edu",
    description="MRI motion artifact rating tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jinghangli98/sphereMRI",
    packages=find_packages(),
    package_data={
        'spheremri': ['*.pt'],
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "torch>=1.7.0",
        "torchvision>=0.8.0",
        "numpy>=1.19.0",
        "pillow>=8.0.0",
        "nibabel>=3.2.0",
        "tqdm>=4.50.0",
    ],
    entry_points={
        "console_scripts": [
            "rate=spheremri.cli:main",
        ],
    },
)
