#!/bin/bash
rm -rf out || exit 0;
mkdir out;
( cd out
 git init
 git config user.name "Travis-CI"
 git config user.email "noreply@travis-ci.org"
 cp -r $TRAVIS_BUILD_DIR/deploy-html/* .
 git add .
 git commit -m "Deployed to Github Pages"
 git push --force --quiet "https://${GH_TOKEN}@${GH_REF}" master:gh-pages > /dev/null 2>&1
)
