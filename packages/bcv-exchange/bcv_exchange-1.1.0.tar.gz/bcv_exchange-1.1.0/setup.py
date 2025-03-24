from setuptools import setup, find_packages

VERSION = '1.1.0'
DESCRIPTION = 'Unofficial Python package to retrieve official exchange rates from the Central Bank of Venezuela (BCV) website.'
PACKAGE_NAME = 'bcv_exchange'
AUTHOR = 'NSMichelJ'
EMAIL = ''
GITHUB_URL = 'https://github.com/NSMichelJ/bcv_exchange'

setup(
    name = PACKAGE_NAME,
    version = VERSION,
    license='MIT',
    description = DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=open('README.md', encoding="utf-8").read(),
    author = AUTHOR,
    author_email = EMAIL,
    url = GITHUB_URL,
    keywords = ['bcv', 'exchange'],
    packages=find_packages(exclude="tests"),
    entry_points={
        'console_scripts': [
            'get_bcv_exchange = bcv_exchange.command:get_bcv_exchange',
        ]
    },
    install_requires=[ 
        'beautifulsoup4==4.13.3',
        'requests==2.32.3'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)