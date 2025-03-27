from setuptools import setup, find_packages

setup(
    name="bi_code",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    author="Ayush Sharma",
    author_email="arksharma528@gmail.com",
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
