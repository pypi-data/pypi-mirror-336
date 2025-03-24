from setuptools import setup, find_packages
setup(
    name="kupala_val", 
    version="1.1.0", 
    author="Maksim Kozyarchuk",
    author_email="maksim.kozyarchuk@gmail.com",
    description="Portfolio valuation, cashflow analysis, and risk assessment.",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kozyarchuk/kupala_val", 
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "kupala_val": ["*.csv"],
    },
    install_requires=[
        "pandas",
        "requests",
    ], 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)