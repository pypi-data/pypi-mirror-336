from setuptools import setup, find_packages

setup(
    name="quicpro",
    version="0.1.0",
    description="A production-ready synchronous pipeline for message transmission with integrated protocol layers.",
    author="Jochen Schultz",
    author_email="js@intelligent-intern.com",
    packages=find_packages(exclude=["tests*"]),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)