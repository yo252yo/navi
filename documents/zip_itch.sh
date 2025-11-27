#!/bin/bash

# Get the current directory name
DIR_NAME=$(basename "$PWD")

rm "${DIR_NAME}_itch.zip"

# Create a zip file excluding the .git directory
zip -r "${DIR_NAME}_itch.zip" . -x ".git/*"

echo "Created ${DIR_NAME}.zip, excluding .git folder."

