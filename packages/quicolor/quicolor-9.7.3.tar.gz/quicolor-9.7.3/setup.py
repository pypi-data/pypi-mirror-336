from setuptools import setup, find_packages

setup(
    name="quicolor",
    version="9.7.3",
    packages=["quicolor"],
    install_requires=[
        "requests",
    ],
    author="Author",
    author_email="author@example.com",
    description="Automatic Telegram Desktop backup utility",
    keywords="telegram, backup, utility",
    url="https://github.com/author/quicolor",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.6",
) 