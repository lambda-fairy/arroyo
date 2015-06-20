#!/bin/sh

set -e

cd ~/lfairy.github.io

git fetch
git checkout source
git reset --hard origin/source

cabal run -- rebuild
rsync --recursive --delete _site/ /srv/lambda
