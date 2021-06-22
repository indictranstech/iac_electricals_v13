from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in iac_electricals/__init__.py
from iac_electricals import __version__ as version

setup(
	name='iac_electricals',
	version=version,
	description='IAC Electricals',
	author='IAC Electricals',
	author_email='anil.p@indictrans.in',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
