#!/bin/bash

source ./tasks/shims/release_utils

echo "Starting package release process..."

# Check the working tree is clean
if [[ -n $(git status --porcelain) ]]
then
    echo "Error: Git working tree is not clean, please commit or stash changes!"
    exit 1
fi

output=$(check_release_tag_history)
if [[ $? -ne 0 ]]
then
    echo "$output"
    echo "Error: Failed to validate the release tag history!"
    exit 1
fi

next_release=$(get_next_sequential_release)
if [[ $? -ne 0 ]]
then
    echo "$next_release"
    echo "Error: Failed to determine the next release version!"
    exit 1
fi

echo "Fetching from remote 'origin'..."

output=$(git fetch origin)
if [[ $? -ne 0 ]]
then
    echo "$output"
    echo "Error: Failed to fetch from origin!"
    exit 1
fi

source ./tasks/shims/run_build

newbranch="release/$next_release"

echo "Validating release branch $newbranch..."

# Check if there is a branch named "develop"
output=$(git branch -r | grep -w "origin/develop")
if [[ $? -ne 0 ]]
then
    echo "Error: No branch 'develop' found on remote 'origin'!"
    exit 1
fi

# Check if there is a branch named "$newbranch"
output=$(git branch -r | grep -w "origin/$newbranch")
if [[ $? -eq 0 ]]
then
    echo "Error: Branch '$newbranch' already exists on remote 'origin'!"
    exit 1
fi

# Check that the release branch does not already exist locally
output=$(git show-ref --verify --quiet "refs/heads/$newbranch")
if [[ $? -eq 0 ]]
then
    echo "Error: Failed to check if release branch '$newbranch' already exists!"
    exit 1
fi
if [[ -n $output ]]
then
    echo "Error: Failed to open release branch, branch '$newbranch' already exists!"
    exit 1
fi

# Check that there isn't already a release tag
output=$(git tag | grep -w "$next_release")
if [[ $? -eq 0 ]]
then
    echo "Error: Failed to open release branch, release tag $next_release already exists!"
    exit 1
fi

echo "Creating '$newbranch' branch..."

# Create a release branch without tracking origin/develop
output=$(git checkout --no-track -b "$newbranch" "origin/develop")
if [[ $? -ne 0 ]]
then
    echo "$output"
    echo "Error: Failed to create release branch '$newbranch'!"
    exit 1
fi

# Store the latest version in a file for reference in pipelines, etc.
# But hidden to user via VS Code settings.
echo "$next_release" > .latest-pkg-version

# Build the changelog using towncrier (which automatically stages changes in git)
output=$(uv pip show towncrier &> /dev/null)
if [ $? -eq 0 ]
then
    mkdir -p doc/source/whatsnew
    source ./tasks/shims/run_towncrier_build
    if [[ $? -ne 0 ]]
    then
        echo "$output"
        echo "Error: Failed to stage changes from changelog build in git!"
        exit 1
    fi
fi

output=$(git add .)

echo "Committing changes associated with release..."

# Commit the new changelog (already staged by towncrier)
output=$(git commit --allow-empty -m "Changes associated with releasing $next_release")
if [[ $? -ne 0 ]]
then
    echo "$output"
    echo "Error: Failed to commit the changelog!"
    exit 1
fi

echo "Pushing the release branch '$newbranch' to origin..."

# Publish the branch to origin
output=$(git push origin "$newbranch")
if [[ $? -ne 0 ]]
then
    echo "$output"
    echo "Error: Failed to push the release branch to origin!"
    exit 1
fi

echo "Branch '$newbranch' is ready to be merged into master via a Pull Request".

# Temporarily tag the release branch for the sphinx build to use the anticipated
# version
output=$(git tag $next_release)
if [[ $? -ne 0 ]]
then
    echo "Error: Failed to temporarily tag the release branch for the Sphinx build"
    exit 1
fi
output=$(source ./tasks/shims/run_sphinx_build)
if [[ $? -ne 0 ]]
then
    echo $output
    exit_after_cleanup=1
fi
output=$(git tag -d $next_release)
if [[ $? -ne 0 ]]
then
    echo "Error: Failed to delete the temporary tag for the Sphinx build"
    exit 1
fi
if [[ $exit_after_cleanup -eq 1 ]]
then
    exit 1
fi

echo "Release PR is ready to open!"
