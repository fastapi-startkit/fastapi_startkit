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
            # NOTE: Remove --dry-run to actually publish
            echo "   Building and publishing $module_name..."
            poetry build
            poetry publish --dry-run
            
            # Return to root
            cd - > /dev/null
            echo "✅ $module_name processed."
            echo "----------------------------------------"
        fi
    done
else
    echo "⚠️  No modules directory found."
fi

# 2. Release Root Package
echo "📦 Releasing root package: fastapi-startkit"
# NOTE: Remove --dry-run to actually publish
poetry build
poetry publish --dry-run

echo "🎉 Release process complete (DRY RUN)!"
echo "ℹ️  To actually publish, edit this script and remove '--dry-run' flags."
