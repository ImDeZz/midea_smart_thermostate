#!/bin/bash

# Function to log messages with timestamp
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') $1"
}

# Navigate to your repository
cd /volume1/home/dezso15/midea_smart_thermostate/midea_smart_thermostate || exit

# Fetch the latest updates from the remote
log "Fetching updates from the remote repository..."
git fetch origin

# Compare the local main branch with the remote main branch
LOCAL=$(git rev-parse main)
REMOTE=$(git rev-parse origin/main)

# Check if the remote branch is ahead
if [ "$LOCAL" != "$REMOTE" ]; then
    log "Local branch is behind. Pulling latest changes..."
    git pull origin main
    log "Pull completed."
else
    log "Local branch is up to date."
fi
