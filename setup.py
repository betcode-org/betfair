import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "requirements.txt")) as f:
    INSTALL_REQUIRES = f.read().splitlines()

with open(os.path.join(here, "requirements-speed.txt")) as f:
    extras_require = f.read().splitlines()
    EXTRAS_REQUIRE = {
        "speed": extras_require,
    }

about = {}
with open(os.path.join(here, "betfairlightweight", "__version__.py"), "r") as f:
    exec(f.read(), about)

with open("README.md", "r") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name=about["__title__"],
    version=about["__version__"],
    packages=[
        "betfairlightweight",
        "betfairlightweight.endpoints",
        "betfairlightweight.resources",
        "betfairlightweight.streaming",
    ],
    package_dir={"betfairlightweight": "betfairlightweight"},
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    url=about["__url__"],
    license=about["__license__"],
    author=about["__author__"],
    author_email="a@unknown.com",
    description=about["__description__"],
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    test_suite="tests",
)
