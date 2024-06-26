#!/bin/bash
#
# This file is part of the JetBrains Manager Tool distribution
# (https://github.com/diogocaveiro/jetbrains-manager-tool).
# Copyright (c) 2024 Diogo Caveiro.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

# This is a helper script used to build the package
# Run this script from the root of the project
# It requires the following tools: tar, fakeroot, dpkg-deb, makepkg

# Set the version
pkgver="0.4.2"

# Other variables
pkgtar="jetbrains-manager-tool_V${pkgver}.tar.gz"
arch_pkg="jetbrains-manager-tool-${pkgver}-1-any.pkg.tar.zst"

# Update package data
today=$(date '+%Y-%m-%d')
sed -i "s/__date__ = \".*\"/__date__ = \"${today}\"/g" jetbrains-manager-tool/jetbrains-manager-tool.py
sed -i "s/__version__ = \".*\"/__version__ = \"${pkgver}\"/g" jetbrains-manager-tool/jetbrains-manager-tool.py
sed -i "1s/.*/JetBrains Manager Tool ${pkgver} (${today})/" jetbrains-manager-tool/docs/help_pages.md
sed -i "s/version = .*/version = \"${pkgver}\"/g" pyproject.toml
sed -i "s/Version: .*/Version: ${pkgver}/g" distro/debian/control


# Package to build
echo "Compressing the package"
tar -cvf "${pkgtar}" jetbrains-manager-tool/ LICENSE CHANGELOG.md poetry.lock pyproject.toml README.md

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

# Convert Arch package to .deb
echo "Converting Arch package to .deb"
mkdir -p deb_tmp/DEBIAN
mkdir -p deb_tmp/usr/share/jetbrains-manager-tool/
tar -xf "${arch_pkg}" -C deb_tmp/
cp ../../distro/debian/control deb_tmp/DEBIAN/
fakeroot dpkg-deb --build deb_tmp/ "jetbrains-manager-tool_${pkgver}_all.deb"
rm -rf deb_tmp/