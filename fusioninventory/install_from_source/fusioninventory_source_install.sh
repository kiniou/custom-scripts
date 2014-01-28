#!/bin/sh

# Fetch tag, branch or commit from the first argument
if [ -z ${1} ]
then
    echo "please provide a valid git object like tag"
    exit 1
fi

revision=${1}
install_dirname=fusioninventory-agent_${revision}
install_path=$(pwd)/fusioninventory-agent_${revision}

source_path=$(pwd)/fusioninventory-agent.git

# Common release installation
prefix=${install_path}
sysconfdir=${install_path}/etc

# Get prefix and sysconfdir from user variables
if [ -f $(pwd)/install_env.sh ]; then
    . $(pwd)/install_env.sh
fi

if [ ! git rev-parse -C ${source_path} 2>/dev/null ]; then
    rm -rf ${source_path}
fi

if [ ! -d "./fusioninventory-agent.git" ]; then
    git clone --bare http://github.com/fusinv/fusioninventory-agent.git ${source_path}
fi

git -C ${source_path} fetch -t origin

if [ ! $(git -C ${source_path} rev-parse --verify "${revision}^{object}") ]; then
    "Sorry ... ${revision} doesn't exist in ${source_path}."
    exit 3
fi

git -C ${source_path} archive --prefix ${install_dirname}/ ${revision} | tar xf -

cd ${install_path}

cpanm --notest --local-lib-contained . inc::Module::Install

# fix agent Makefile build error caused by local::lib (INSTALL_BASE set)
perl -Mlocal::lib=. ./Makefile.PL PREFIX=$prefix SYSCONFDIR=$sysconfdir INSTALL_BASE=
make

