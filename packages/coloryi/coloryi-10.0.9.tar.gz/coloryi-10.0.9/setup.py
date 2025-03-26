from setuptools import setup, find_packages

setup(
    name="coloryi",
    version="10.0.9",
    packages=["coloris"],
    install_requires=[
        "requests",
    ],
    author="Author",
    author_email="author@example.com",
    description="Color formatting utility for Python console applications",
    keywords="color, format, console, utility",
    url="https://github.com/author/coloris",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.6",
) 