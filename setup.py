import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="fiuba-taller-2-app-server",
    version="1.00",
    author="Romina Casal",
    author_email="casal.romina@gmail.com",
    description="FIUBA - 7552 - 1C2020 - Grupo 8",
    license="GPLv3",
    keywords="ChoTuve AppServer",
    url="https://github.com/romicasal/fiuba-taller-2-app-server",
    packages=[
        '',
        'src',
        'src.clients',
        'src.conf',
        'src.misc',
        'src.models',
        'src.resources',
        'src.schemas',
        'src.services',
        'tests',
        'tests.test_schemas',
        'tests.test_utils'],
    install_requires=read('requirements.txt'),
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Education",
        "License :: GPLv3 License",
    ],
)
