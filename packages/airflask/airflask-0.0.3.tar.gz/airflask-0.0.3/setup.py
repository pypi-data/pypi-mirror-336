from setuptools import setup, find_packages

setup(
    name="airflask",  
    version="0.0.3",
    author="Naitik Mundra",
    author_email="naitikmundra18@gmail.com",
    description="Simplest way to host your flask web app!",
    url="https://github.com/naitikmundra/FlaskAir",
    packages=find_packages(), 
    install_requires=[
        "flask",
        "click",
    ],
    entry_points={
        "console_scripts": [
            "airflask=airflask.__main__:cli",  
        ],
    }

)
