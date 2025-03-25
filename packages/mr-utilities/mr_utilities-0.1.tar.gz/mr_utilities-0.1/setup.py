from setuptools import setup, find_packages  

setup(  
    name='mr_utilities',  
    version='0.1',  
    packages=find_packages(),  
    description='Different utility functions for data processing',  
    author='Majid Rouhani',  
    author_email='majid.rouhani@ntnu.no',  
    url='https://git.ntnu.no/rouhani/utilities',  
    classifiers=[  
        'Programming Language :: Python :: 3',  
        'License :: OSI Approved :: MIT License',  
        'Operating System :: OS Independent',  
    ],  
    python_requires='>=3.6',  
)  