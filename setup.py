from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in ecs_vehicles/__init__.py
from ecs_vehicles import __version__ as version

setup(
	name="ecs_vehicles",
	version=version,
	description="ecs_vehicles",
	author="ecs_vehicles",
	author_email="ecs_vehicles",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
