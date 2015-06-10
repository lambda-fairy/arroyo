#!/bin/sh

set -e

cd /home/chris/public/website

git fetch
git reset --hard origin/source

cabal run -- rebuild
rsync --recursive --delete _site/ /var/www/lambda
