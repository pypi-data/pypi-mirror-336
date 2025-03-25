from setuptools import setup, find_packages

setup(
    name="backgen",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "click",
        "fastapi",
        "pytest",
    ],
    entry_points={
        "console_scripts": [
            "backgen=backgen.cli:cli",
        ],
    },
)
