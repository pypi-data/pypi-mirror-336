#!/bin/bash

# -----------------------------------------------------------------------------
# Builds a zip lambda image
# -----------------------------------------------------------------------------

# Requires: sudo apt update && sudo apt install -y libcurl4-openssl-dev libssl-dev zlib1g-dev zip

# Declare variables
PLATFORM="x86_64-manylinux2014"
PYTHON_VERSION="3.12"

echo "Bumping version ..."
v=$(uvx --from=toml-cli toml get --toml-path=pyproject.toml project.version)
# bump patch version
part="patch"
uvx --from bump2version bumpversion --allow-dirty --current-version "$v" "$part" pyproject.toml

BASE_VERSION=$(uvx --from=toml-cli toml get --toml-path=pyproject.toml project.version)
echo "✅ Bumped version to $BASE_VERSION"

echo "Deleting old folders ..."
# Create dist folder
mkdir -p dist/build

# Delete old files
rm -rf dist/build/*
rm -f dist/*.zip
rm -f dist/*.txt
echo "✅ Deleted old folders"

echo "Building the image for multiple platforms"
uv export --frozen --no-dev --no-editable -o dist/requirements.txt
uv pip install --no-cache-dir --no-installer-metadata --no-compile-bytecode --python-platform ${PLATFORM} --python ${PYTHON_VERSION} --target dist/build -r dist/requirements.txt

echo "Packaging the image"
cd dist/build
zip -r ../package.${BASE_VERSION}.zip .
echo "✅ Packaged the image"
