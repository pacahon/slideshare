from setuptools import setup, find_packages
import sys, os

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


def get_requirements():
    return open('requirements.txt').read().splitlines()

long_description = read('README.md')

setup(
    name='slideshare',
    version="0.0.2",
    description="Slideshare API client",
    author='Sergey Zherevchuk',
    author_email='pacabest@gmail.com',
    long_description=long_description,
    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords=['slideshare', 'api'],
    url='https://github.com/pacahon/python-slideshare',
    license='LGPL',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=get_requirements(),
    tests_require=['pytest'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],
)
