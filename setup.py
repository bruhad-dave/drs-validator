import os
from setuptools import setup, find_packages
HERE = os.path.dirname(__file__)

version = "0.0.1"
description = "Submission for GA4GH Technical Interview."

setup(name = "drs_validator",
        packages = find_packages(),
        version = version, description = description,
        long_description = "DRS Object Endpoint Tests; "+description)
