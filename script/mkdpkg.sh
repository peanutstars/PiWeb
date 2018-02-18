#!/bin/bash

DPKG_DIR=$PIWEB_ROOT_DIR/dpkg
VERSION_FILE=$PIWEB_SRC_DIR/core/version.py
DPKG_CONTROL_FILE=$DPKG_DIR/DEBIAN/control

Version=`cat $VERSION_FILE | grep "return" | grep "\"" | awk -F\" '{ print $2 }'`
Package="piweb"
Architecture="unknown"
InstalledSize=`du --max-depth=0 $DPKG_DIR | awk '{ print $1 }'`


checkArchitecture() {
	# Arch=`uname -m`
	# case "$Arch" in
	# 	x86_64)
	# 		Architecture="amd64"
	# 		;;
	# 	armv7l|armv6l)
	# 		Architecture="armhf"
	# 		;;
	# 	*)
	# 		Architecture="unknown"
	# 		;;
	# esac
	# [ "$Architecture" == "unknown" ] && echo -e "\n\tArchitecture is unknown.\n" && exit 1
	Architecture="all"
}

generateControl() {
	cat >$DPKG_CONTROL_FILE <<EOF
Package: $Package
Version: $Version
Depends: python3, python3-pip, libncurses5-dev, libreadline-dev, virtualenv
Priority: optional
Architecture: $Architecture
Section: Network
Installed-Size: $InstalledSize
Maintainer: Peanutstars <peanutstars.dev@gmail.com>
Description: This is a simple web server to be used the cherrypy
 ...
EOF
}

checkArchitecture
generateControl
pushd $PIWEB_ROOT_DIR
fakeroot dpkg --build dpkg
mv dpkg.deb $Package-$Version-$Architecture.deb
popd
