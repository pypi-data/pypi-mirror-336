from setuptools import setup, find_packages

setup(
    name="pyvoa_full",  
    version="0.1.1",  
    author="pyvoa.org",
    author_email="contact@pyvoa.org",
    description="Python virus open analysis, full version. See more on pyvoa.org",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/pyvoa/pyvoa_full",  # Link to github deposit
    packages=find_packages(), 
    install_requires=[
        "pyvoa",
        "bokeh",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",  # Version minimale de Python
)
