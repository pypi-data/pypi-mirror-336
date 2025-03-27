# setup.py

from setuptools import setup, find_packages

setup(
    name='my_calculator_library',       # Name of your library
    version='0.1.0',                    # Version of your library
    packages=find_packages(),           # Finds all packages and sub-packages
    install_requires=[],                # External dependencies (leave empty for now)
    test_suite='tests',                 # Test suite location
    author='Muhammad Raheel',                 # Your name
    author_email='mraheel.naseem@gmail.com', # Your email
    description='A simple calculator library', # Short description
    long_description=open('README.md').read(), # Detailed description
    long_description_content_type='text/markdown', # Format of the README
    url='https://github.com/muhammadraheelnaseem', # Repository URL
    classifiers=[                       # Python version and license information
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
