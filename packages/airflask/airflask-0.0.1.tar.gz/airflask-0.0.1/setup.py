from setuptools import setup, find_packages

setup(
    name="airflask",  # Change to your package name
    version="0.0.1",
    author="Naitik Mundra",
    author_email="naitikmundra18@gmail.com",
    description="Simplest way to host your flask web app!",
    url="https://github.com/naitikmundra/FlaskAir",
    packages=find_packages(),
    install_requires=[
       "flask"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
