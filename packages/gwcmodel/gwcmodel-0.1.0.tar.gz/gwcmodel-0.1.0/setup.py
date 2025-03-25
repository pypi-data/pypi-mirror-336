from setuptools import setup, find_packages

setup(
    name="gwcmodel",
    version="0.1.0",
    author="Goodwill Wealth Management Pvt Ltd",
    author_email="apisupport@gwcindia.in",
    description="Python SDK for GWC India API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
