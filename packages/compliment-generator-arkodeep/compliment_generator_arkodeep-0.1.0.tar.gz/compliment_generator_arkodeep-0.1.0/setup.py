from setuptools import setup, find_packages

setup(
    name="compliment_generator_arkodeep",
    version="0.1.0",
    author="Arkodeep Kundu",
    author_email="arkodeepkundu11@gmail.com",
    description="A simple compliment generator",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Arkodeep120611/compliment_generator",
    packages=find_packages(),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
