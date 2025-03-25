from setuptools import setup, find_packages

with open("README.md", "r") as file:
    description = file.read()

setup(
    name="si-dyno-reader",
    version='0.0.2',
    packages=find_packages(),
    install_requires=[
        'numpy==2.0.2'
    ],
    long_description=description,
    long_description_content_type="text/markdown"
)