from setuptools import setup, find_packages
# read the contents of README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="roofline-plotter",
    version="0.1.1",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "matplotlib>=3.5",
        "numpy>=1.21",
    ],
    python_requires=">=3.8",
    description="A simple roofline plotter for visualizing performance data",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="chickenjohn",
    author_email="chickenjohn93@outlook.com",
    url="https://github.com/chickenjohn/roofline-plotter",
)
