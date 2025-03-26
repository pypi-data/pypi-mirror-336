from setuptools import setup, find_packages

setup(
    name="roofline-plotter",
    version="0.1.0",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "matplotlib>=3.5",
        "numpy>=1.21",
    ],
    python_requires=">=3.8",
    description="A simple roofline plotter for visualizing performance data",
    author="chickenjohn",
    author_email="chickenjohn93@outlook.com",
    url="https://github.com/chickenjohn/roofline-plotter",
)
