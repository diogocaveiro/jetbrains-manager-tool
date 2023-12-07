#!/bin/bash

# Set the version
pkgver="0.4.0"

# Other variables
pkgtar="jetbrains-manager-tool_V${pkgver}.tar.gz"

# Update script data
today=$(date '+%Y-%m-%d')
sed -i "s/__date__ = \".*\"/__date__ = \"${today}\"/g" jetbrains-manager-tool/jetbrains-manager-tool.py
sed -i "s/__version__ = \".*\"/__version__ = \"${pkgver}\"/g" jetbrains-manager-tool/jetbrains-manager-tool.py

# Package to build
echo "Compressing the package"
tar -cvf "${pkgtar}" jetbrains-manager-tool/ LICENSE CHANGELOG poetry.lock pyproject.toml README.md

# Create directories
echo "Creating the directories"
mkdir -p "release/${pkgver}"
mv "${pkgtar}" "release/${pkgver}"
cp PKGBUILD "release/${pkgver}"
cd "release/${pkgver}" || return

# Checksum
echo "Creating the checksum"
sha256sum "jetbrains-manager-tool_V$pkgver.tar.gz" > "jetbrains-manager-tool_V$pkgver.tar.gz.sha256sum"
checksum=$(sha256sum ${pkgtar} | cut -f 1 -d " ")

# Replace the checksum
echo "Replacing the checksum in PKGBUILD"
sed -i "s/PACKAGE_CHECKSUM/${checksum}/g" PKGBUILD
sed -i "s/PACKAGE_VERSION/${pkgver}/g" PKGBUILD

# Build the package
echo "Building the package"
makepkg -sc