#!/bin/bash

if [ ! -n "${GOPATH}" ]; then
    echo "You need to install golang and you should've configured your GOPATH environment variable."
    exit 1
fi

if [ $# != 4 ]; then
    echo "You need input APIKEY, ServerCert, PrivateKey, Version"
    exit 1
fi

if [ ! -f "${2}" ] || [ ! -f "${3}" ]; then
    echo "ServerCert and PrivateKey file must exists."
    exit 1
fi

APIKEY=${1}
ServerCert=${2}
PrivateKey=${3}
Version=${4}
gitversion=""

if [ $Version != "master" ]; then
    if [[ ${Version:0:1} -ne "v" ]]; then
        Version=v${4}
    fi
    gitversion="-b "${Version}
fi
echo "API-KEY is ${APIKEY}, ServerCert is ${ServerCert}, PrivateKey is ${PrivateKey}, Version is ${Version}"


current_branch() {
    dir=$1
    if [ -d $dir/.git ]; then
        cat $dir/.git/HEAD | awk -F "/" '{print $3}'
    else
        echo -1
    fi
}

# $1 = dir; $2 = branch-name
exist_branch() {
    dir=$1
    branch=$2
    if [ -f $dir/.git/refs/heads/$branch ]; then
        echo 1
    else
        echo 0
    fi

}

readonly axn_dir=${GOPATH}/src/github.com/arxanchain/
if [ ! -d "${axn_dir}" ]; then
    mkdir -p ${axn_dir}
fi

echo "start wallet-sdk-py"
if [ ! -d "${axn_dir}/wallet-sdk-py" ]; then
    echo "git clone wallet-sdk-py"
    cd ${axn_dir}
    git clone ${gitversion} https://github.com/arxanchain/wallet-sdk-py.git
else
    echo "already wallet-sdk-py"
    cd ${axn_dir}/wallet-sdk-py
    git pull
    isExist=$(exist_branch "." $Version)
    if [ $isExist ne 0 ]; then
        cur=$(current_branch ".")
        if [ "$cur"x != "$Version"x ]; then
            echo "$Version branch already exist, checkout it"
            git checkout $Version
        else
            echo "already on branch $Version"
        fi
        git pull
    else
        echo "$Version branch not exist, create it"
        git checkout -b ${Version} origin/${Version}
    fi
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

echo "start sdk-go-common utils.so"
echo "rm exists tools dir"
if [ -d "${axn_dir}/sdk-go-common/crypto/tools/library" ]; then
    cd ${axn_dir}/sdk-go-common/crypto/tools/library
    rm -fr build
fi

echo "make..."
cd ${axn_dir}/sdk-go-common/crypto/tools/library;make

echo "prepare utils path"
readonly pyc_install_path=$(python -c 'import imp;print imp.find_module("cryption")[1]')
if [ -z "${pyc_install_path}" ]; then
    exit 2
fi

if [ ! -d "${pyc_install_path}/utils" ]; then
    mkdir -p ${pyc_install_path}/utils
fi
echo "utils path: ${pyc_install_path}/utils"
echo "copy utils.so to utils path"
cp -f ${axn_dir}sdk-go-common/crypto/tools/library/build/utils.so ${pyc_install_path}/utils
echo "utils.so copy succeed."

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
