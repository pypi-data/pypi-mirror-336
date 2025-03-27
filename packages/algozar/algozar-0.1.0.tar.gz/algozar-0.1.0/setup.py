from setuptools import setup, find_packages

setup(
    name="algozar",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],  
    author="Izzar Suly Nashrudin",
    author_email="Izzarsuly@proton.me",
    description="Collection of algorithm designs and some code to help ease the running of the program.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/avezoor/algozar",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Unix"
    ],
    python_requires='>=3.6',
)
