from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="hotpod-cli",
    version="0.1.0",
    author="JDCloud AIDC Team",
    author_email="your.email@example.com",
    description="A command line tool for GCS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/hotpod-cli",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "click>=7.0",
    ],
    entry_points={
        "console_scripts": [
            "hotpod=hotpod_cli.cli:cli",
        ],
    },
)
