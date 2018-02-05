#!/usr/bin/env python

from setuptools import setup, find_packages
import io

with open('./requirements.txt') as reqs_txt:
    requirements = [line for line in reqs_txt]

setup(
    name='wallet-sdk-py',
    version='1.5.0',
    description="Python SDKs for Blockchain Wallet",
    long_description=io.open('README.md', encoding='utf-8').read(),
    url='https://github.com/arxanchain/wallet-sdk-py/',
    download_url='https://github.com/arxanchain/wallet-sdk-py/',
    packages=find_packages(),
    platforms='any',
    install_requires=requirements,
    include_package_data=True,
    zip_safe=False,
)
