#!/bin/bash
GH_USER_NAME="$(git --no-pager show -s --format='%an' HEAD)"
GH_USER_EMAIL="$(git --no-pager show -s --format='%ae' HEAD)"
COMMIT_ID="$(git rev-parse --short HEAD)"

(cd $TRAVIS_BUILD_DIR/deploy-html && \
 git init && \
 git config user.name $GH_USER_NAME && \
 git config user.email $GH_USER_EMAIL && \
 git add . && \
 git commit -m "Travis-CI -> gh-pages: $(date) from ${COMMIT_ID}" && \
 git push --force --quiet "https://${GH_TOKEN}@${GH_REF}" master:gh-pages > /dev/null 2>&1
)
