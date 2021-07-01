#!/usr/bin/env bash
if [ $# -ne 1 ]; then
    echo "Usage: $0 <csl3 username>"
    exit 1
fi
mv ./finalCheck src/
rsync -azv "$1@csl3.cs.technion.ac.il:~mtm/public/2021b/ex3/*" src/
mv src/finalCheck .
