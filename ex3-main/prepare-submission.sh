#!/usr/bin/env bash

NAME=submission_test.zip
FINAL=ex3.zip

zip "${NAME}" -j src/gradesCalc.py

./finalCheck "${NAME}"

rm -i "${NAME}"
if [ -f "${NAME}" ]; then
    echo "Saving ${NAME} as ${FINAL}"
    mv "${NAME}" "${FINAL}"
fi
