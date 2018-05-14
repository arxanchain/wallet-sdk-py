#!/bin/bash

if [ ! -n "${GOPATH}" ]; then
    echo "You need to install golang and you should've configured your GOPATH environment variable."
    exit 1
fi

if [ $# != 3 ]; then
    echo "You need input APIKEY, ServerCert, PrivateKey"
    exit 1
fi

if [ ! -f "${2}" ] || [ ! -f "${3}" ]; then
    echo "ServerCert and PrivateKey file must exists."
    exit 1
fi

APIKEY=${1}
ServerCert=${2}
PrivateKey=${3}
echo "API-KEY is ${APIKEY}, ServerCert is ${ServerCert}, PrivateKey is ${PrivateKey}"

readonly axn_dir=${GOPATH}/src/github.com/arxanchain/
if [ ! -d "${axn_dir}" ]; then
    mkdir -p ${axn_dir}
fi

echo "start wallet-sdk-py"
if [ ! -d "${axn_dir}/wallet-sdk-py" ]; then
    echo "git clone wallet-sdk-py"
    cd ${axn_dir}
    git clone https://github.com/arxanchain/wallet-sdk-py.git
else
    echo "already wallet-sdk-py"
    cd ${axn_dir}/wallet-sdk-py
    git pull
fi

echo "start install wallet-sdk-py (include py-common)"
cd ${axn_dir}/wallet-sdk-py
pip install -r requirements.txt
python setup.py install
echo "wallet-sdk-py project install succeed."

echo "start sdk-go-common"
if [ ! -d "${axn_dir}/sdk-go-common" ]; then
    echo "git clone sdk-go-common"
    cd ${axn_dir}
    git clone https://github.com/arxanchain/sdk-go-common.git
else
    echo "already sdk-go-common"
    cd ${axn_dir}/sdk-go-common
    git pull
fi

echo "start sdk-go-common crypto-util and sign-util"
echo "rm exists tools dir"
if [ -d "${axn_dir}/sdk-go-common/crypto/tools" ]; then
    cd ${axn_dir}/sdk-go-common/crypto/tools
    rm -fr build
fi

echo "make..."
cd ${axn_dir}/sdk-go-common/crypto/tools;make

echo "prepare utils path"
readonly pyc_install_path=$(python -c 'import imp;print imp.find_module("cryption")[1]')
if [ -z "${pyc_install_path}" ]; then
    exit 2
fi

if [ ! -d "${pyc_install_path}/utils" ]; then
    mkdir -p ${pyc_install_path}/utils
fi
echo "utils path: ${pyc_install_path}/utils"
echo "copy crypto-util and sign-util to utils path"
cp -f ${axn_dir}sdk-go-common/crypto/tools/build/bin/crypto-util ${pyc_install_path}/utils
cp -f ${axn_dir}sdk-go-common/crypto/tools/build/bin/sign-util ${pyc_install_path}/utils
echo "crypto-util and sign-util copy succeed."

echo "start certs/tls/tls.cert and certs/users/API-KEY/API-KEY.key"
echo "prepare certs dir"
if [ ! -d "${pyc_install_path}/ecc/certs/tls" ]; then
    mkdir -p ${pyc_install_path}/ecc/certs/tls
fi
if [ ! -d "${pyc_install_path}/ecc/certs/users/${APIKEY}" ]; then
    mkdir -p ${pyc_install_path}/ecc/certs/users/${APIKEY}
fi

echo "copy ServerCert and PrivateKey to certs path"
cp -f ${ServerCert}  ${pyc_install_path}/ecc/certs/tls/tls.cert
cp -f ${PrivateKey}  ${pyc_install_path}/ecc/certs/users/${APIKEY}/${APIKEY}.key
echo "tls.cert and API-KEY.key copy succeed."

echo "all wallet-sdk-py env prepare succeed."
