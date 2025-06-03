#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Define colors for better readability
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting build process...${NC}"

# Remove existing docs folder content
echo -e "${GREEN}Cleaning docs/ directory...${NC}"
rm -rf docs/*
mkdir -p docs

# Run the Python static site generator
echo -e "${GREEN}Generating site with base path /StaticSiteGenerator/...${NC}"
python3 src/main.py "/StaticSiteGenerator/"

echo -e "${GREEN}Build complete!${NC}"
