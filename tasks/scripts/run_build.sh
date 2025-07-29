#!/bin/bash

output=$(uv build 2>&1)
if [ $? -ne 0 ]
then
    echo "$output"
    echo "Error: Failed to build project!"
    exit 1
fi
