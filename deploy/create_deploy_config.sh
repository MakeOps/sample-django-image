#!/usr/bin/env bash

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --image-url)
            IMAGE_URL="$2"
            shift 2
            ;;
        --commit-hash)
            COMMIT_HASH="$2"
            shift 2
            ;;
        --output)
            OUTPUT="$2"
            shift 2
            ;;
        *)
            echo "Unknown argument: $1"
            exit 1
            ;;
    esac
done

# Validate required arguments
if [ -z "$IMAGE_URL" ] || [ -z "$COMMIT_HASH" ] || [ -z "$OUTPUT" ]; then
    echo "Usage: $0 --image-url <image-url> --commit-hash <commit-hash> --output <output-file>"
    exit 1
fi

# Get current timestamp
BUILD_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Create JSON output
cat > "$OUTPUT" << EOF
{
    "imageUri": "$IMAGE_URL:$COMMIT_HASH",
    "commitHash": "$COMMIT_HASH",
    "buildTime": "$BUILD_TIME"
}
EOF
