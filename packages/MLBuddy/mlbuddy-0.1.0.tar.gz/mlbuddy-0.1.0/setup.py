from setuptools import setup, find_packages

setup(
    name="MLBuddy", 
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.20.0",
        "scikit-learn>=1.0.0",
        "tqdm>=4.62.0",
        "lightgbm>=3.3.0",
        "xgboost>=1.5.0",
        "seaborn>=0.11.0",
        "matplotlib>=3.4.0"  
    ],
    author="Neilansh Chauhan",
    author_email="neilanshchauhan4@gmail.com",  # Add your email if you want
    description="A simple AutoML library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    # url="https://github.com/yourusername/MLBuddy",  # Add your repository URL
    license="MIT",
    python_requires=">=3.7",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
)
