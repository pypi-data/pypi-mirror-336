from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="package_teste_pacotes",
    version="0.0.1",
    author="Fábio Alves",
    author_email="fabio.dp.alves@gmail.com",
    description="Teste de Criação de Pacotes",
    long_description=page_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/fabiodpa/simple-package-template"
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)
