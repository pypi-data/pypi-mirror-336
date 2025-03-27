import pathlib
from platform import python_version

from setuptools import setup,find_packages

setup(name="greeksoft",
      version='0.0.4',
      description="The official Python client for communicating with Greeksoft's CTCL Application API",
      long_description=pathlib.Path("README.md").read_text(),
      long_description_content_type='text/markdown',
      author="Greek_dev_Team",
      author_email='greeksoftapi@greeksoft.co.in',
      license="MIT License",
      packages=find_packages(),
      install_requires=[
            'requests>=2.32.3',
            'pandas>=1.19.5',
            'websocket-client>=1.8.0'
      ],
      python_version="=>3.10",
      include_package_data=True,

      )