from setuptools import setup, find_packages
setup(
    name = "chewcorp",
    version = "0.0.1",
    packages = find_packages(),
    install_requires=[
        'httplib2>=0.9.1',
        'google-api-python-client',
    ],
    entry_points={
        'console_scripts': [
            'cdns=chewcorp.dns:run',
        ],
    } 
)
