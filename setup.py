from setuptools import setup, find_packages
setup(
    name = "chewcorp",
    version = "0.0.1",
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
