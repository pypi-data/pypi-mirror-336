from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '10.0.2'
DESCRIPTION = 'Dependency confiuse Test'
LONG_DESCRIPTION = 'hello world'

# Setting up
setup(
    name="pyrovider",
    version=VERSION,
    author="shiphero",
    author_email="hello@shiphero.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['socket','getpass'],
    keywords=[]
   )
