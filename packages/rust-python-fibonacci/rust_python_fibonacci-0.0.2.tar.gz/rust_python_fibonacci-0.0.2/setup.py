import pathlib
from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

with open(str(pathlib.Path(__file__).parent.absolute()) +
          "/version.py", "r") as fh:
    version = fh.read().split("=")[1].replace("'", "")

setup(
    name="rust_python_fibonacci",
    version=version,
    author="SportyGeek2015",
    author_email="this_is_not_a_real_emall_address@hotmail.com",
    description="Calculates a Fibonacci number",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SportyGeek2015/rust_python_fibonacci",
    install_requires=[
        "PyYAML>=4.1.2",
        "dill>=0.2.8"
    ],
    extras_require={
     'server': ["Flask>=1.0.0"]
    },
    packages=find_packages(exclude=("tests",)),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'fib-number = rust_python_fibonacci.cmd.fib_numb:fib_numb',
        ],
    },
    python_requires='>=3.10',
    tests_require=['pytest'],
)