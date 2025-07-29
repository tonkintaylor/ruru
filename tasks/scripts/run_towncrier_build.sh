#!/bin/bash

source ./tasks/shims/activate_venv

output=$(uv pip show towncrier &> /dev/null)
if [ $? -eq 0 ]
then
    echo "Building the changelog using towncrier..."

    # Read the version from .latest-pkg-version
    if [ ! -f ".latest-pkg-version" ]
    then
        # If the file does not exist, create it with a default version
        echo "v0.0.0" > .latest-pkg-version
        echo "Created .latest-pkg-version with default version v0.0.0"
    fi
    next_release=$(cat .latest-pkg-version)

    if [ -z "$next_release" ]
    then
        echo "Error: Failed to read the release version from .latest-pkg-version !"
        exit 1
    fi

    output=$(uv run towncrier build --yes --version $next_release)
    if [ $? -ne 0 ]
    then
        echo "$output"
        echo "Error: Failed to build the changelog with Towncrier!"
        exit 1
    fi

    echo "Built Changelog!"
fi
