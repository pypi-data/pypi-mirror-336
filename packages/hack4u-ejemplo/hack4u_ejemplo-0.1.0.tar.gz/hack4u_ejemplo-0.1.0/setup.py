from setuptools import setup, find_packages

#Leer el contenido del archivo README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="hack4u_ejemplo",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="Carlos Reyes",
    description="Una biblioteca para consultar cursos de hack4u",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://hack4u.io",
)
