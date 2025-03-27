from setuptools import setup, find_packages

setup(
    name="clinicaltrials_interact",
    version="0.1.8",
    packages=find_packages(),
    install_requires=[
    "requests>=2.32.3,<3.0.0",
    "pandas>=2.2.0,<3.0.0",
    "sentence-transformers>=3.4.1,<4.0.0",
    "scikit-learn>=1.6.1,<2.0.0",
    "matplotlib>=3.10.1,<4.0.0",
    "seaborn>=0.13.2,<1.0.0",
    "plotly>=5.0.0",
    # Add other runtime dependencies as needed...
    ],
    author="KeyVuLee",
    description="A Python package to interact with ClinicalTrials.gov API v2",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/hsph-bst236/midterm-project-keyvulee-innovations/tree/api/clinicaltrials_interact",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6, <3.13',
)