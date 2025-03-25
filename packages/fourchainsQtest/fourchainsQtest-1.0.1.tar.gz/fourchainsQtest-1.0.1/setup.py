from setuptools import setup, find_packages

setup(
    name="fourchainsQtest",
    version="1.0.1",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "requests",
        "pydantic",
        "pyngrok",
        "flask"
    ],
    author="fourchains",
    author_email="fourchains.work@gmail.com",
    description="fourchainsQtest",
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)