from setuptools import setup, find_packages

setup(
    name="autoPyEnV",  # Updated package name
    version="0.1.0",
    packages=find_packages(),
    install_requires=["click"],
    entry_points={
        "console_scripts": [
            "env=env.cli:cli",
        ],
    },
    author="Your Name",
    description="An automated Python environment management tool",
    url="https://github.com/WolvarineXD/autoPyEnV",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
