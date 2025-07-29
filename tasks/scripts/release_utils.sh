#!/bin/bash

# Find current git tag history
RELEASE_FMT="^v[0-9]+\.[0-9]+\.[0-9]+$"
RELEASE_FMT_MSG="vX.Y.Z"

check_format_release() {
    # Check that the release tags match the required format
    local release=$1

    if ! [[ "$release" =~ $RELEASE_FMT ]]
    then
        echo "Error: Release tag $release does not match the format $RELEASE_FMT_MSG"
        exit 1
    fi
}

chunk_release() {
    # Split a release tag into its major, minor, and micro components as an array
    local release=$1

    check_format_release "$release"

    # Get number components of each release
    local major=$(echo "$release" | cut -d. -f1 | cut -dv -f2)
    local minor=$(echo "$release" | cut -d. -f2)
    local micro=$(echo "$release" | cut -d. -f3)

    local chunks=( $major $minor $micro )

    echo "${chunks[@]}"
}

check_nodupl_releases() {
    # Check that there are no duplicate release tags
    local releases=$1

    local dupl_tags=$(echo "$releases" | uniq -d)

    if ! [ -z "$dupl_tags" ]
    then
        echo "Error: Duplicate release tags detected: run `git tag --list`"
        exit 1
    fi
}

le_release() {
    # Compare two release tags: return whether the first is less than or equal to the second
    local release1=$1
    local release2=$2

    local chunks1=($(chunk_release "$release1"))
    local chunks2=($(chunk_release "$release2"))

    for ((i=0; i<${#chunks1[@]}; i++))
    do
        if ! [[ ${chunks1[$i]} -eq ${chunks2[$i]} ]]
        then
            if [[ ${chunks1[$i]} -lt ${chunks2[$i]} ]]
            then
                return 0
            else
                return 1
            fi
        fi
    done

    return 0
}

check_are_ordered_releases() {
    # Check that the release tags are in the correct order,
    # i.e. release 1 is newer than release 2
    local release1=$1
    local release2=$2

    if ! (le_release "$release1" "$release2")
    then
        echo "Error: Release tag $release1 is out of order with respect to $release2"
        exit 1
    fi
}

are_sequential_releases() {
    # Check that two release tags are sequential
    local release1=$1
    local release2=$2

    local chunks1=($(chunk_release "$release1"))
    local chunks2=($(chunk_release "$release2"))

    # Loop over the chunks. c1 should be equal to c2, until you hit a case where
    # c1 != c2, at which point it should hold that c1 + 1 == c2 and that thereafter,
    # c2 == 0
    local chunk_count=${#chunks1[@]}
    for ((i=0; i<chunk_count; i++))
    do
        local chunk1=${chunks1[$i]}
        local chunk2=${chunks2[$i]}
        if ! [[ $chunk1 -eq $chunk2 ]]
        then
            if [[ $chunk1 -eq $((chunk2 - 1)) ]]
            then
                for ((j=i+1; j<chunk_count; j++))
                do
                    local chunks2=${chunks2[$j]}
                    if ! [[ chunks2 -eq 0 ]]
                    then
                        return 1
                    fi
                done
                return 0
            else
                return 1
            fi
        fi
    done

    return 1
}

check_are_sequential_releases() {
    # Check that the release tags are sequential, and warn the user if not
    local release1=$1
    local release2=$2

    if ! (are_sequential_releases "$release1" "$release2")
    then
        # Check the user wants to have a non-sequential release
        if [[ -t 0 ]]
        then
            echo "Warning: Release tag $release1 is not sequential with respect to $release2"
            echo "Do you want to continue? [y/N]"
            local response=$(read -r)
        else
            echo "Error: Release tag $release1 is not sequential with respect to $release2!"
            exit 1
        fi

        case $response in
            [yY])
                :
                ;;
            [nN] | *)
                echo "Aborting"
                exit 1
                ;;
        esac
    fi
}



check_consecutive_releases() {
    # Check that the release tags are in the correct order and are sequential
    # N.B. the releases must be provided sorted by commit date, oldest first
    local releases=$1

    local release2=""
    for release1 in $releases
    do
        if ! [ -z "$release2" ]
        then
            check_are_ordered_releases "$release1" "$release2"
            check_are_sequential_releases "$release1" "$release2"
        fi

        release2="$release1"
    done
}

get_release_tag_history() {
    # Get the release tag history sorted by commit date, oldest first
    history=$(git tag --sort=-creatordate)
    echo "$history"
}

check_release_tag_history() {
    # Check that the release tags are valid
    local tag_history=$(get_release_tag_history)

    check_nodupl_releases "$tag_history"
    check_consecutive_releases "$tag_history"
}

get_latest_release() {
    # Get the latest release tag
    local tag_history=$(get_release_tag_history)

    echo "$tag_history" | head -n 1
}

get_next_major_release() {
    # Get the next major release tag
    local major=$1

    echo "v$(($major + 1)).0.0"
}

get_next_minor_release() {
    # Get the next minor release tag
    local major=$1
    local minor=$2

    echo "v$major.$(($minor + 1)).0"
}

get_next_micro_release() {
    # Get the next micro release tag
    local major=$1
    local minor=$2
    local micro=$3

    echo "v$major.$minor.$(($micro + 1))"
}

get_next_custom_release() {
    # Get the next custom release tag based on user input
    local major=$1
    local minor=$2
    local micro=$3

    if [[ -t 0 ]]
    then
        echo "Enter the next release tag:"
        local response=$(read -r)
    else
        echo "Error: cannot get user input to query custom tag!"
        exit 1
    fi

    # Validate the release tag
    check_format_release "$response"
    check_are_ordered_releases "v$major.$minor.$micro" "$response"
    check_are_sequential_releases "v$major.$minor.$micro" "$response"

    echo "$response"
}

get_next_sequential_release() {
    # Get the next release tag based on user input.

    local latest_release=$(get_latest_release)

    local next_release
    if [ -z "$latest_release" ]
    then
        local response
        if [[ -t 0 ]]
        then
            local query="No release tags found. Do you want to release the first version as v0.1.0? [Y/n]"
            read -p "$query" response
        else
            response="Y"
        fi

        case $response in
            [yY])
                :
                ;;
            [nN] | *)
                echo "Aborting"
                exit 1
                ;;
        esac

        next_release="v0.1.0"
    else
        local chunks=($(chunk_release "$latest_release"))

        local major="${chunks[0]}"
        local minor="${chunks[1]}"
        local micro="${chunks[2]}"

        local next_major_release=$(get_next_major_release "$major")
        local next_minor_release=$(get_next_minor_release "$major" "$minor")
        local next_micro_release=$(get_next_micro_release "$major" "$minor" "$micro")

        # Ask the user what kind of release they want, potentially allowing a custom,
        # non-sequential release
        local release_type_prompt="What kind of release do you want?
        1. Major release ($latest_release -> $next_major_release)
        2. Minor release ($latest_release -> $next_minor_release)
        3. Micro release ($latest_release -> $next_micro_release)
        4. Custom release
        Enter a number [1-4]: "
        release_type_prompt=$(echo "$release_type_prompt" | sed "s/^[[:space:]]*//")

        local response
        if [[ -t 0 ]]
        then
            read -p "$release_type_prompt" response
        else
            response="3"
        fi


        case $response in
            1)
                next_release="$next_major_release"
                ;;
            2)
                next_release="$next_minor_release"
                ;;
            3)
                next_release="$next_micro_release"
                ;;
            4)
                next_release=$($get_release_func "$major" "$minor" "$micro")
                ;;
            *)
                echo "Error: Invalid response $response"
                exit 1
                ;;
        esac
    fi

    echo "$next_release"
}
