from setuptools import setup, find_packages

setup(
    name="auledft",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "ase",
        "numpy",
        "click",
        "streamlit",  # Se usi Streamlit
    ],
    entry_points={
        "console_scripts": [
            "auledft=auledft.cli:cli",
        ],
    },
)
