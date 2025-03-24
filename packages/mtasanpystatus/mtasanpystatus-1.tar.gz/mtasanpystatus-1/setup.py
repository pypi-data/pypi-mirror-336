from setuptools import setup, find_packages

setup(
    name='mtasanpystatus',
    version='1',
    packages=find_packages(),
    install_requires=[], 
    author='ieoub',
    author_email='rib7daily@gmail.com',
    description='A library for monitoring MTA:SA servers.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ieoub/mtasanpystatus',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)