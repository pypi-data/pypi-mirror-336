from setuptools import setup, find_packages

setup(
    name="PyORM-Lite",
    version="1.0.0",
    author="sby-devapp",
    author_email="sbydev.app@gmail.com",
    description="A lightweight Python ORM for SQLite databases.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sby-devapp/PyORM.git",
    packages=find_packages(),
    install_requires=[],  # Add dependencies here if needed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
