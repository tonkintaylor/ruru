#!/bin/bash

# Read the version from the .latest-pkg-version file
if [ ! -f ".latest-pkg-version" ]
then
    # If the file does not exist, create it with a default version
    echo "v0.0.0" > .latest-pkg-version
    echo "Created .latest-pkg-version with default version v0.0.0"
fi
release_name=$(cat .latest-pkg-version)
if [[ $? -ne 0 ]]
then
    echo "Error: Could not read the release version from .latest-pkg-version"
    exit 1
fi

output=$(git fetch --tags)
if [[ $? -ne 0 ]]
then
    echo "$output"
    echo "Error: Could not fetch tags from origin"
    exit 1
fi

tagname=${branchname/release\//}
if git rev-parse -q --verify "refs/tags/$tagname" > /dev/null
then
    echo "Error: Tag $tagname already exists, will not overwrite. Please manage the tags manually."
    exit 1
fi

output=$(git tag -am "Release $release_name" "$release_name")
if [[ $? -ne 0 ]]
then
    echo "$output"
    echo "Error: Could not tag release $release_name"
    exit 1
fi

output=$(git push origin "$release_name")
if [[ $? -ne 0 ]]
then
    echo "$output"
    echo "Error: Could not push release tag $release_name to origin"
    exit 1
fi
