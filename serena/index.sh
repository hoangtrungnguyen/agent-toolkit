#!/bin/bash
set -e

# Ensure the container is running
if ! docker ps | grep -q serena-container; then
    echo "Serena container is not running. Please start it with 'docker compose up -d'"
    exit 1
fi

# Fetch available projects from the running container's /workspace folder
echo "Fetching available projects in /workspace..."
# Use tr to convert newlines to spaces for the select array
projects=$(docker exec serena-container ls /workspace 2>/dev/null)

if [ -z "$projects" ]; then
    echo "No projects found in /workspace. Check your docker-compose.yaml volume mounts."
    exit 1
fi

echo "Please select a project to index:"
# Convert the projects string into an array
project_array=()
while IFS= read -r line; do
    [ -n "$line" ] && project_array+=("$line")
done <<< "$projects"

select project in "${project_array[@]}" "Exit"; do
    if [ "$project" == "Exit" ]; then
        echo "Exiting..."
        exit 0
    elif [ -n "$project" ]; then
        echo "=========================================="
        echo "🚀 Indexing project: $project"
        echo "=========================================="
        # Run the indexing command interactively inside the container
        docker exec -it serena-container bash -c "source .venv/bin/activate && serena project index /workspace/$project"
        echo "Done!"
        break
    else
        echo "Invalid selection. Please enter a valid number."
    fi
done
