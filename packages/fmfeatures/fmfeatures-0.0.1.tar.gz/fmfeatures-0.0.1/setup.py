# Import required functions
from setuptools import setup, find_packages

# Call setup function
setup(
    author="Gabriel Palma",
    description="FMFeatures is a Python package that provides a comprehensive set of tools for extracting features from finance market time series data. It is designed to simplify feature engineering in financial analysis and machine learning applications.",
    name="fmfeatures",
    packages=find_packages(include=["src", "fmfeatures.*"]),
    version="0.0.1",
    install_requires=[
        'numpy', 
        'pandas', 
        'scipy', 
        'hmmlearn', 
        'mclustpy', 
        'rpy2', 
        'TA-Lib', 
        'scikit-learn'],
    extras_require={
        'tensorflowMac': ['tensorflow==2.15.0', 
                          'tensorflow-metal==1.1.0',],        
    }
)
