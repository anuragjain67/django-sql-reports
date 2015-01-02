import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-sqlreports',
    version='0.1',
    author='Anurag',
    author_email='anurag.jain@hashedin.com',
    description='Write SQL to generate sqlreports',
    license='MIT',
    keywords="django report sql",
    url='https://github.com/anuragjain67/django-sql-reports',
    packages=find_packages(),
    include_package_data=True,
    long_description=README,

    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
    install_requires=[]
)
