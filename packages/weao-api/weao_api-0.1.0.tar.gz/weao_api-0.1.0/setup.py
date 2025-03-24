from setuptools import setup, find_packages

setup(
    name="weao_api",
    version="0.1.0",
    author="Flames",
    author_email="correywheatley6@gmail.com",
    description="A Python package for interacting with the WEAO API.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/FlamesIsCool/weao_api",  # Change to your repository URL
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)
