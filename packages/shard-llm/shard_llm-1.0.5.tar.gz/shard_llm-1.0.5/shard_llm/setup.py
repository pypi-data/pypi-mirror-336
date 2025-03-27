from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="llamaforge",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A package for fine-tuning LLMs to behave like specific characters",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/llamaforge",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "torch>=2.0.0",
        "transformers>=4.30.0",
        "peft>=0.4.0",
        "datasets>=2.10.0",
        "accelerate>=0.20.0",
        "bitsandbytes>=0.40.0",
    ],
)