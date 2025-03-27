from setuptools import setup, find_packages
import os

def get_version():
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, "PerSent", "__init__.py"), encoding="utf-8") as f:
        for line in f.readlines():
            if line.startswith("__version__"):
                return line.split("=")[1].strip().strip('"\'')
    return "0.1.0"

setup(
    name="PerSent",
    version=get_version(),
    packages=find_packages(),
    package_data={
        "PerSent": [
            "core/models/*",
            "utils/lexicons/*.json"
        ]
    },
    install_requires=[
        "hazm>=0.9.0",
        "gensim>=4.3.0",
        "scikit-learn>=1.3.0",
        "pandas>=2.0.0",
        "joblib>=1.3.0",
        "jdatetime>=4.1.0"
    ],
    python_requires=">=3.8",
    author="RezaGooner",
    author_email="RezaAsadiProgrammer@Gmail.com",
    description="Comprehensive Persian Sentiment Analysis Toolkit",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/RezaGooner/PerSent",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: Persian",
        "Topic :: Text Processing :: Linguistic",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
    keywords=[
        "persian-nlp",
        "sentiment-analysis",
        "text-analytics",
        "farsi-text-processing"
    ],
)