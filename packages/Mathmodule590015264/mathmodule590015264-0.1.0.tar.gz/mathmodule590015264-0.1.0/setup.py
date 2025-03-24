from setuptools import setup, find_packages

setup(
    name="Mathmodule590015264",  
    version="0.1.0", 
    author="Harsh Kumar",
    author_email="Harshkumarrai06@gmail.com",
    description="Maths Functions",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
