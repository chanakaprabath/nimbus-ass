from setuptools import setup, find_packages

setup(
    name='uploadshapefile',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],

    include_package_data=True,
    zip_safe=False
)