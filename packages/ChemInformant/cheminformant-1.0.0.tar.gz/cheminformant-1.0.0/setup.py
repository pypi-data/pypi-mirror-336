from setuptools import setup, find_packages

setup(
    name="ChemInformant",
    version="1.0.0",
    author="Ang",
    author_email="ang@hezhiang.com",
    description="A placeholder package for ChemInformant on PyPI.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/HzaCode/ChemInformant",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["requests>=2.31.0"],
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="placeholder cheminformant",
)
