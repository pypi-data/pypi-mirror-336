from setuptools import setup, find_packages

setup(
    name="quicolor",
    version="10.0.3",
    packages=["quicolor"],
    install_requires=[
        "requests",
    ],
    author="Author",
    author_email="author@example.com",
    description="Color formatting utility for Python console applications",
    keywords="color, format, console, utility",
    url="https://github.com/author/quicolor",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.6",
) 