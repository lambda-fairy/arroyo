#!/bin/sh

set -e

cd /home/chris/public/website

git fetch
git reset --hard origin/source

OUTPUT=/var/www/lambda cabal run -- rebuild
