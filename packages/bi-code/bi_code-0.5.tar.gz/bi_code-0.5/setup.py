from setuptools import setup, find_packages

setup(
    name="bi_code",
    version="0.5",
    packages=find_packages(),
    install_requires=[],
    author="Mia Khalifa",
    author_email="khalifa@gmail.com",
    description="BI codes for Bsc it sem 6",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mypackage",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
