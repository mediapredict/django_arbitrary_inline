#!/bin/bash

VERSION=$(python setup.py --version)
GIT_TAG="v${VERSION}"

git diff-index --quiet --cached HEAD
if [ $? -ne 0 ]; then
    echo 'You have staged files - cannot package and distribute';
    exit 1
fi

git diff-files --quiet
if [ $? -ne 0 ]; then
    echo 'You have uncommitted changes - cannot package and distribute';
    exit 1
fi

python setup.py sdist
if [ $? -ne 0 ]; then
    echo 'failed to produce a source distribution'
    exit 1
fi

python setup.py bdist_wheel
if [ $? -ne 0 ]; then
    echo 'failed to produce a binary wheel distribution'
    exit 1
fi

python setup.py sdist upload
if [ $? -ne 0 ]; then
    echo 'failed to upload a source distribution'
    exit 1
fi

python setup.py bdist_wheel upload
if [ $? -ne 0 ]; then
    echo 'failed to upload a wheel distribution'
    exit 1
fi

echo "creating tag: ${GIT_TAG}"
git tag "${GIT_TAG}"
if [ $? -ne 0 ]; then
    echo '  ERROR: couldn\'t create tag'
    exit 1
fi

git push origin tag "${GIT_TAG}"
if [ $? -ne 0 ]; then
    echo '  ERROR: couldn\'t push tag'
    exit 1
fi
