#!/bin/bash

BUILD_DIR=./build

pushd "$(dirname ${BASH_SOURCE:0})" || exit 1
trap popd EXIT
# locate in the root of the sub-project
cd ..

# check if directory build exists
if [ -d "${BUILD_DIR}" ]; then
	rm -r "${BUILD_DIR}"
fi

mkdir "${BUILD_DIR}"
cd "${BUILD_DIR}"

# Build
cmake ..
make