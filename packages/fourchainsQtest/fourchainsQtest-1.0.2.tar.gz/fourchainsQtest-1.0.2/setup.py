from setuptools import setup, find_packages

setup(
    name="fourchainsQtest",
    version="1.0.2",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "requests",
        "pydantic",
        "pyngrok",
        "flask"
    ],
    package_data={
        '': [
            'config.py', 
            'requirements.txt',
            'qxenonsign/__init__.py',
            'qxenonsign/core.py',
            'qxenonsign/pyarmor_runtime_000000/__init__.py',
            'qxenonsign/pyarmor_runtime_000000/pyarmor_runtime.pyd'
        ],
    },
    include_package_data=True,
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