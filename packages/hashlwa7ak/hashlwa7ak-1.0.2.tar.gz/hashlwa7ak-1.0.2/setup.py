from setuptools import setup, find_packages

setup(
    name='hashlwa7ak',
    version="1.0.2",
    packages=find_packages(),
    install_requires=[
        'requests',
        'paramiko',
        'beautifulsoup4',
        'rich'
    ],
    entry_points={
        'console_scripts': [
            'hashlwa7ak=hashlwa7ak_pkg.cli_main:main',
        ],
    },
)
