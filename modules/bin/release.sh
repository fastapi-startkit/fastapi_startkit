#!/bin/bash

# Exit on error
set -e

echo "🚀 Starting release process..."

# 1. Release Modules
MODULES_DIR="modules"

if [ -d "$MODULES_DIR" ]; then
    for module in "$MODULES_DIR"/*; do
        if [ -d "$module" ] && [ -f "$module/pyproject.toml" ]; then
            module_name=$(basename "$module")
            echo "📦 Releasing module: $module_name"

            # Navigate to module directory
            cd "$module"

            # Build and Publish
            echo "   Building and publishing $module_name..."
            poetry build
            poetry publish

            # Return to root
            cd - > /dev/null
            echo "✅ $module_name processed."
            echo "----------------------------------------"
        fi
    done
else
    echo "⚠️  No modules directory found."
fi
