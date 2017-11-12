import sys
from setuptools import setup


if sys.version_info < (2, 6):
    print 'ERROR: simple_plugins requires at least Python 2.6 to run.'
    sys.exit(1)


setup(
    name='simple_plugins',
    version='1.0.2',
    url='https://bitbucket.org/petar/simple_plugins',
    license='BSD',
    author='Petar Maric',
    author_email='petarmaric@uns.ac.rs',
    description='A simple plugin framework',
    long_description=open('README').read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],
    platforms='any',
    py_modules=['simple_plugins'],
    setup_requires = ['nose>=1.0'],
    tests_require = [
        'coverage>=3.3', 'friendly_name_mixin>=1.0', 'nose>=1.0',
        'nosexcover>=1.0.7', 'nose_extra_tools>=1.0'
    ],
    test_suite = 'nose.collector',
)
