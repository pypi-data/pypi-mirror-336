from setuptools import setup, find_packages

setup(
    name="image-padder",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "Pillow",
        "tqdm",
    ],
    entry_points={
        "console_scripts": [
            "image-padder=image_padder.main:main",
        ],
    },
    author="crapthings",
    author_email="crapthings@gmail.com",
    description="A command-line tool to pad and resize images",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/crapthings/py-image-padder",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)