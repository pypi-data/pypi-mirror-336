from setuptools import setup, find_packages

setup(
    name="codelingo",
    version="0.1",
    author="Taksh Kamble/Sahil Patil/Ashish Ghodvinde/Bhishek Zope",
    author_email="ghodvindeashish@gmail.com",
    description="A library to convert code snippets into plain English.",
    long_description=open("Readme.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AshishGhodvinde/CodeLingo",
    packages=find_packages(),  # Automatically finds the 'codelingo' package
    install_requires=[],       # List dependencies here (if any)
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Specify Python version compatibility
)