from setuptools import setup, find_packages

# Read the long description from your README file.
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="DrugAutoML",
    version="0.0.4",
    author="Ayça Beyhan & Aslı Suner",
    author_email="aycapamukcu9@gmail.com",
    description="DrugAutoML: An Open-Source Automated Machine Learning and Statistical Evaluation Tool for Bioactivity Prediction in Drug Discovery",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aycapmkcu/DrugAutoML",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "scikit-learn",
        "matplotlib",
        "seaborn",
        "rdkit",
        "shap",
        "xgboost",
        "lightgbm",
        "hyperopt"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    license="MIT"
)
