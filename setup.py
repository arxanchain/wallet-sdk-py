#!/usr/bin/env python

from setuptools import setup, find_packages
import io

setup(
    name='wallet-sdk-py',
    version='1.5.0',
    description="Python SDKs for Blockchain Wallet.",
    long_description=io.open('README.md', encoding='utf-8').read(),
    url='https://github.com/arxanchain/wallet-sdk-py/',
    download_url='https://github.com/arxanchain/wallet-sdk-py/',
    packages=find_packages(),
    platforms='any',
    install_requires=[
        "certifi",
        "chardet==3.0.4",
        "funcsigs==1.0.2",
        "idna==2.6",
        "mock==2.0.0",
        "pbr==3.1.1",
        "requests==2.18.4",
        "six==1.11.0",
        "timeout-decorator==0.4.0",
        "urllib3==1.22",
        "py-common==v1.5",
        "httpretty==0.8.14"
    ],
    dependency_links=[
        "git+git://github.com/arxanchain/py-common.git#egg=py-common-v1.5",
        "git+git@github.com:gabrielfalcao/HTTPretty.git#egg=httpretty-0.8.14"

    ],
    include_package_data=True,
    zip_safe=False,
)
