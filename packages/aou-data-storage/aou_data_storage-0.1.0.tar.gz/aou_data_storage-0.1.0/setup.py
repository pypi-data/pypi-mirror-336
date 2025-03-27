
from setuptools import setup, find_packages
setup(
    name='aou_data_storage',
    version='0.1.0',
    author='Aymone Jeanne Kouame',
    author_email='aymone.jk@gmail.com',
    description='aou_data_storage is a package that contains functions to move data from a Google Cloud Workspace persistent disk to its bucket or from two different buckets.',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        ],
    python_requires='>=3.6',
)
