#!/usr/bin/env python

from setuptools import setup, find_packages
import io

setup(
    name='wallet-sdk-py',
    version='2.1.2',
    description="Python SDKs for Blockchain Wallet.",
    long_description=io.open('README.md', encoding='utf-8').read(),
    url='https://github.com/arxanchain/wallet-sdk-py/',
    download_url='https://github.com/arxanchain/wallet-sdk-py/',
    packages=find_packages(),
    platforms='any',
    install_requires=[
        "certifi==2018.1.18",
        "chardet==3.0.4",
        "funcsigs==1.0.2",
        "idna==2.6",
        "mock==2.0.0",
        "pbr==3.1.1",
        "requests==2.20.0",
        "six==1.11.0",
        "timeout-decorator",
        "urllib3==1.22",
        "py-common"
        ],
    dependency_links=[
        "git+git://github.com/arxanchain/py-common.git@v2.1.2#egg=py-common-v2.0.1"
    ],
    include_package_data=True,
    zip_safe=False,
)
