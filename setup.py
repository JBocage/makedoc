"""The setup file for the project
"""

import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

from src.makedoc import __VERSION__

setup(
    name="makedoc",
    version=".".join([str(v) for v in __VERSION__]),
    description="auto doc generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="J. Bocage",
    author_email="julien.bocage@gmail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3.8",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7, <4",
    # This field lists other packages that your project depends on to run.
    # Any package you put here will be installed by pip when your project is
    # installed, so they must be valid existing projects.
    #
    # For an analysis of "install_requires" vs pip's requirements files see:
    # https://packaging.python.org/discussions/install-requires-vs-requirements/
    install_requires=[],  # Optional
    # List additional groups of dependencies here (e.g. development
    # dependencies). Users will be able to install these using the "extras"
    # syntax, for example:
    #
    #   $ pip install sampleproject[dev]
    #
    # Similar to `install_requires` above, these must be valid existing
    # projects.
    extras_require={  # Optional
        "dev": [],
        "test": [],
    },
    # If there are data files included in your packages that need to be
    # installed, specify them here.
    package_data={"": ["./src/makedoc/cli/commands/bash_scripts/*"]},  # Optional
    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/distutils/setupscript.html#installing-additional-files
    #
    # In this case, 'data_file' will be installed into '<sys.prefix>/data'
    entry_points={"console_scripts": ["makedoc = makedoc.cli.main:cli"]},
)
