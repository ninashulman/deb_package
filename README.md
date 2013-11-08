# -----------------------------------------------------------------------------------------
# How to build a debian package for Ubuntu
# -----------------------------------------------------------------------------------------

# Step 1 
# Clone the content of https://github.com/ninashulman/deb_package into package_name-1.0/
$ git clone https://github.com/ninashulman/deb_package package_name-1.0
# Cloned package_name-1.0 directory consist of debian\ and DEBIAN\ which were produced by running
#               dh_make -e youremail@address -f ../package_name-1.0.orig.tar.gz
#               and altered to fit the info needed for future building and installation of the package

# Step 2
# Create directory for source code inside of package_name-1.0/
$ cd package_name-1.0/
$ mkdir -p usr/share/package_name

# Step 3
# Unzip the source directory content into package_name-1.0/usr/share/package_name/

# Step 4
# Update the Architecture line in the debian/control file to match the one used on the client machine
# If in doubt, on the client machine run $ uname -i  
# Example of the line to include in the control file: 
#       Architecture: i386

# Step 5
# Check that you have usr/, debian/ , DEBIAN/, and README.md , inside package_name-1.0/

# Step 6
# Build a source package package_name_1.0-1.dsc
$ cd package_name-1.0/
$ debuild -S
#   click y for yes when prompted   

# Step 7
# Go up to package_name-1.0/ and observe package_name_1.0-1.dsc being created there 
$ cd ..

# Step 8
# Build a binary debian package package_name_1.0-1_i386.deb in the current directory
$ dpkg-deb -b package_name-1.0 .

# Done! package_name_1.0-1_i386.deb is ready to be used  for installation on Ubuntu machine
# You may rup dpkg -I (with capital I) to see info about this package: $ dpkg -I  package_name_1.0-1_i386.deb

# ------------------------------------------------------------------------------------------------------
# How to install a debian package on Ubuntu machine
# ------------------------------------------------------------------------------------------------------

# Step 1
# Run $ uname -i to make sure that your package was built for your hardware platform architecture
#                   For i386, use package_name_1.0-1_i386.deb
#                   For amd64, use package_name_1.0-1_amd64.deb


# Step 2
# Install the package onto the client machine
$ sudo dpkg -i  package_name_1.0-1_i386.deb

# Step 3
# How to check where the package was installed and more info if needed
 $ dpkg -L package_name
 $ dpkg --status  package_name
 $ dpkg -I package_name_version.deb  #that -I must be capital

# Done! Package is installed
# Package can be easily uninstalled by running $ sudo apt-get remove package_name

