from setuptools import setup, find_packages

setup(
    name="unraid-api",
    version="0.1.0",
    description="Python library for Unraid GraphQL API",
    author="Ruaan Deysel",
    author_email="ruaan.deysel@gmail.com",
    url="https://github.com/domalab/pyunraid",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "httpx>=0.23.0",
        "pydantic>=2.0.0",
        "graphql-core>=3.2.0",
        "typeguard>=2.13.0",
        "websockets>=10.3",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.18.0",
            "pytest-cov>=3.0.0",
            "black>=23.0.0",
            "isort>=5.10.0",
            "mypy>=0.950",
        ],
    },
)
