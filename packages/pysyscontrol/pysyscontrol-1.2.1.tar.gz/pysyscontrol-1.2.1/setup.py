from setuptools import setup, find_packages
import os

def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename), encoding="utf-8") as f:
        return f.read()

setup(
  name="pysyscontrol",
  version="1.2.1",
  author="Shagedoorn1",
  author_email="svenhagedoorn@gmail.com",
  description="A Python package for Control Systems Analysis",
  license_files=["LICENSE"],
  long_description=read_file("README.md") + "\n\n" + read_file("CHANGELOG.md"),
  url="https://github.com/Shagedoorn1/PySysControl",
  long_description_content_type="text/markdown",
  packages=find_packages(),
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  python_requires=">=3.12"
)