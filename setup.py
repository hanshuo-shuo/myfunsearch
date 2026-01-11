"""Setup script for MyFunSearch package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="myfunsearch",
    version="0.1.0",
    author="hanshuo-shuo",
    description="LLM-powered evolution of mice behavior in predator-prey environments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hanshuo-shuo/myfunsearch",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        # Core package has no external dependencies
    ],
    extras_require={
        "llm": [
            "openai>=1.0.0",
            "anthropic>=0.7.0",
        ],
        "viz": [
            "matplotlib>=3.5.0",
            "numpy>=1.21.0",
        ],
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "mypy>=0.990",
        ],
    },
    entry_points={
        "console_scripts": [
            "funsearch-basic=funsearch.examples.basic_example:main",
            "funsearch-viz=funsearch.examples.visualization_example:main",
            "funsearch-advanced=funsearch.examples.advanced_example:main",
        ],
    },
)
