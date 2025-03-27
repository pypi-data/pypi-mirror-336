from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="flashbots_header_signer",
    version="0.1.1",
    author="SeriouS",
    author_email="onium16@gmail.com",
    description="Utility for creating signed headers for Flashbots requests, ensuring Web3 version compatibility.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/onium16/flashbots-header-signer",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    install_requires=[
        "aiohttp>=3.8.0",
        "web3>=6.0.0",
        "eth_account>=0.5.9",
        "requests>=2.27.1",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-asyncio",
            "pytest-cov",  # For test coverage
            "black",       # Code formatting
            "flake8",      # Code linting
            "aioresponses", # Mocking async requests
        ],
    },
    python_requires=">=3.9",
    license="MIT",
)
