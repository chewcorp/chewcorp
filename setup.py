from setuptools import setup, find_packages

import chewcorp
version = chewcorp.__version__

setup(
    name = "chewcorp",
    version = version,
    packages = find_packages(),
    install_requires=[
        'cement',
        'httplib2>=0.9.1',
        'google-api-python-client',
    ],
    entry_points={
        'console_scripts': [
            'chewcorp=chewcorp.cli.app:run',
        ],
    } 
)
