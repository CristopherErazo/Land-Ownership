#!/usr/bin/env bash

# Makefile for Sphinx documentation

set -e

SPHINXBUILD=sphinx-build
SOURCEDIR=source
BUILDDIR=build

if [ "$#" -eq 0 ]; then
    echo "Usage: make.sh [target]"
    echo "Targets: html, latexpdf, linkcheck, clean"
    exit 1
fi

"$SPHINXBUILD" -M "$@" "$SOURCEDIR" "$BUILDDIR"
