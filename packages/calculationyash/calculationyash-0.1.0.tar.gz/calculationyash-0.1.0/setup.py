from setuptools import setup, find_packages

setup(
    name="calculationyash",  # Package name on PyPI
    version="0.1.0",  # Package version
    packages=find_packages(),  # Automatically find all packages
    install_requires=[],  # Dependencies (if any)
    author="Yash Sharma",
    author_email="yash.innovater@gmail.com",
    description="A pakage which can calculate",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yash-sharma3/calculationyash",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimum Python version
)