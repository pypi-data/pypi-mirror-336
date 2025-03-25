from setuptools import setup, find_packages

setup(
    name="SeriesMaster",  # Your library name
    version="0.2.2",  # Version number
    author="Aditya",  # Your name
    description="A Python library for various mathematical series operations",
    long_description=open("README.md").read(),  # Reads from README.md
    long_description_content_type="text/markdown",
    packages=find_packages(),  # Automatically find all modules
    install_requires=[
        "matplotlib",  
        "P",
        
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimum Python version
    entry_points = {
        "console_scripts":[
            "SeriesMaster-ReadMe = SeriesMaster:ReadMe"
        ]
    }
)
