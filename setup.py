from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name="chemical-formula-parser",
      version="0.0.1",
      description="A python package to parse chemical formula",
      long_description=long_description,
      long_description_content_type="text/markdown",
      author="lquastana",
      packages=["chemical_formula_parser"],
      install_requires=["lark"],
      platforms='any',
      license="Apache 2.0")