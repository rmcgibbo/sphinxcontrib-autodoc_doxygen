#!/bin/bash -e
git config --global user.email "$(git --no-pager show -s --format='%ae' HEAD)"
git config --global user.name "$(git --no-pager show -s --format='%an' HEAD)"
COMMIT_ID="$(git rev-parse --short HEAD)"

TEMPDIR=$(mktemp -d)
trap "rm -rf ${TEMPDIR}" EXIT

cd $TEMPDIR
git clone -b gh-pages --single-branch "https://${GH_REF}" gh-pages
cp -rf $TRAVIS_BUILD_DIR/deploy-html/* gh-pages/
cd gh-pages
git add .
git commit -m "Travis-CI deploy ${COMMIT_ID} to gh-pages" && \
git push --force --quiet "https://${GH_TOKEN}@${GH_REF}" master:gh-pages > /dev/null 2>&1

