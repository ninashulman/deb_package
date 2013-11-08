-----------------------------------------------------------------------------------------
How to build stackstorm-capacity debian package for Ubuntu
-----------------------------------------------------------------------------------------

# Step 1 
# Clone the content of https://github.com/ninashulman/deb_package into stackstorm-capacity-1.0/
$ git clone https://github.com/ninashulman/deb_package stackstorm-capacity-1.0
# Cloned stackstorm-capacity-1.0 directory consist of debian\ and DEBIAN\ which were produced by running
#		dh_make -e youremail@address -f ../stackstorm-capacity-1.0.orig.tar.gz 
#		and altered to fit the info needed for future building and installation of the package

# Step 2
# Create directory for source code inside of stackstorm-capacity-1.0/
$ cd stackstorm-capacity-1.0/
$ mkdir -p usr/share/stackstorm-capacity

# Step 3
# Unzip the capacity directory content into stackstorm-capacity-1.0/usr/share/stackstorm-capacity
#	from https://www.dropbox.com/s/qesmj2yyqbv1xxe/capacity-dashboard.tar.gz

# Step 4
# Update the Architecture line in the debian/control file to match the one used on the client machine
# If in doubt, on the client machine run $ uname -i  
# Example of the line to include in the control file: 
#	Architecture: i386

# Step 5
# Check that you have usr/, debian/ , DEBIAN/, and README.md , inside stackstorm-capacity-1.0/

# Step 6
# Build a source package stackstorm-capacity_1.0-1.dsc
$ cd stackstorm-capacity-1.0/
$ debuild -S
#   click y for yes when prompted   

# Step 7
# Go up to stackstorm-capacity-1.0/ and observe stackstorm-capacity_1.0-1.dsc being created there 
$ cd ..

# Step 8
# Build a binary debian package stackstorm-capacity_1.0-1_any.deb in the current directory
$ dpkg-deb -b stackstorm-capacity-1.0 . 

# Done! stackstorm-capacity_1.0-1_i386.deb is ready to be used  for installation on Ubuntu machine
# Your may rup dpkg -I (with capital I) to see info about this package: $ dpkg -I  stackstorm-capacity_1.0-1_i386.deb

------------------------------------------------------------------------------------------------------
How to install the stackstorm-capacity package on Ubuntu machine
------------------------------------------------------------------------------------------------------

# Step 1
# Run $ uname -i to make sure that your package was built for your hardware platform architecture
#		    For i386, use stackstorm-capacity_1.0-1_i386.deb
#		    For amd64, use stackstorm-capacity_1.0-1_amd64.deb


# Step 2
# Install the package onto the client machine
$ sudo dpkg -i  stackstorm-capacity_1.0-1_i386.deb

# Step 3
# How to check where the package was installed and more info if needed
 $ dpkg -L stackstorm-capacity
 $ dpkg --status  stackstorm-capacity
 $ dpkg -I archive_file_name.deb  #that -I must be capital
 
# Done! Package is installed
# Package can be easily uninstalled by running $ sudo apt-get remove stackstorm-capacity
