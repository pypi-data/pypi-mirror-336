from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ks_openai",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.32.3",
        "pydantic>=2.0.0"
    ],
    description="A Python wrapper for OpenAI-like API with custom access key management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Raj Aryan",
    author_email="raj@klopudstac.com",
    url="https://github.com/mr-rsr/ks_openai",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)