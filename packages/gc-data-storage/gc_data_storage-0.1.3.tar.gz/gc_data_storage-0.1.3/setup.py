
from setuptools import setup, find_packages
setup(
    name='gc_data_storage',
    version='0.1.3',
    author='Aymone Jeanne Kouame',
    author_email='aymone.jk@gmail.com',
    description=" 'gc_data_storage' is a package that contains functions to move data from a Google Cloud Workspace persistent disk to its bucket, or between two different Workspace buckets. It was created to be used within the All of Us Researcher Workbench by default. More information, including README, at https://github.com/AymoneKouame/gc_data_storage",
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        ],
    python_requires='>=3.6',
)
