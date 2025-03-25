from setuptools import setup, find_packages

setup(
    name="cryptocodemanipal",
    version="0.2.0",
    author="SAM",
    author_email="samyakbargale12@gmail.com",
    description="A collection of cryptographic algorithms",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/SamyakBargale/cryptocodemanipal",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "sympy",  # Example dependency
        "tinyec",
        "pycryptodome",
        "cryptography",
    ],
    python_requires=">=3.6",
)