#!/bin/bash
set -e

# Ensure the container is running
if ! docker ps | grep -q serena-container; then
    echo "Serena container is not running. Please start it with 'docker compose up -d'"
    exit 1
fi

echo "=========================================="
echo "   Checking Index Status of Projects      "
echo "=========================================="

# Fetch available projects from the running container's /workspace folder
projects=$(docker exec serena-container ls /workspace 2>/dev/null)

if [ -z "$projects" ]; then
    echo "No projects found in /workspace. Check your docker-compose.yaml volume mounts."
    exit 1
fi

project_array=()
while IFS= read -r line; do
    [ -n "$line" ] && project_array+=("$line")
done <<< "$projects"

for project in "${project_array[@]}"; do
    if [ -n "$project" ]; then
        # Check if the cache directory exists inside each project 
        has_cache=$(docker exec serena-container bash -c "if [ -d /workspace/$project/.serena/cache ]; then echo 'yes'; else echo 'no'; fi")
        if [ "$has_cache" == "yes" ]; then
            printf "✅  %-25s : Indexed\n" "$project"
        else
            printf "❌  %-25s : Not Indexed\n" "$project"
        fi
    fi
done

echo "=========================================="
