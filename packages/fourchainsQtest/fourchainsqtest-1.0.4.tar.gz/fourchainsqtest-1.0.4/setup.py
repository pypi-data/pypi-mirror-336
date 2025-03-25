from setuptools import setup, find_packages

setup(
    name="fourchainsQtest",
    version="1.0.4",
    packages=find_packages(include=['qxenonsign', 'qxenonsign.*']),
    install_requires=[
        "numpy",
        "requests",
        "pydantic",
        "pyngrok",
        "flask"
    ],
    include_package_data=True,
    package_data={
        'qxenonsign': ['config.py'],  # config.py를 qxenonsign에 포함
    },
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
