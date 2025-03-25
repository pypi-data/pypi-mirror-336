from setuptools import setup, find_packages
import os.path

here = os.path.dirname(__file__)

descr_file = os.path.join(here, "README.md")
version_file = os.path.join(here, "src", "farfetchd", "__version__.py")

version_info = {}
with open(version_file, "r") as f:
    exec(f.read(), version_info)

dev_requirements = [
    "black",
    "Jinja2",
    "pylint",
]

setup(
    name=version_info["__title__"].lower(),
    version=version_info["__version__"],
    packages=find_packages("src", exclude=["test"]),
    package_dir={"": "src"},
    description=f"{version_info['__title__']} is an asynchronous wrapper around the pokeapi.co API",
    long_description=open(descr_file).read(),
    author=version_info["__author__"],
    url="https://github.com/pseudonym117/farfetchd",
    classifiers=[],
    license="MIT",
    install_requires=["aiohttp"],
    extras_require={"dev": dev_requirements},
)
