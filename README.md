# ####################
# How to set GPGKEY if you do not have it (needed for signing deb packages)
# ####################
# Step 0
$ sudo apt-get install pgp gnupg-agent 

# Step 1
# To help generating GPG key, get ready to run in a separace shell (on the same machine)
$ find / &gt; /dev/null   
# run it while you are generating gpgkey in the next step and kill this process after GPG key is generated

# Generate gpgkey
$ gpg --gen-key --no-use-agent 
# option 4 ( RSA (sign only), use defaults)
# Observe your gpgkey being generated and save its value
# Example:  key 6A25F155 marked as ultimately trusted

# Step 2
# check that your genkey is listed
$ gpg --list-secret-keys
# Example:
# /home/ninas/.gnupg/secring.gpg
# -----------------------------
# sec   2048R/6A25F155 2013-10-29
# uid     Nina Shulman <ninas@saasbook.com>

# Step 3
# Add your gpgkey to ~/.bashrc file
# Example of line in  ~/.bashrc file:  export GPGKEY=6A25F155

# Step 4
#Now restart the gpg-agent and source your .bashrc again:	
$ killall -q gpg-agent
$ eval $(gpg-agent --daemon)
$ source ~/.bashrc

# Step 5
# check that keys set correctly to the value your exported in ~/.bashrc file
$ echo $GPGKEY

# ####################
# How to build stackstorm-capacity debian package for Ubuntu
# ####################
# Step 0
$ sudo apt-get install devscripts

# Step 1 
# Clone the content of https://github.com/ninashulman/deb_package into package_name-1.0/
$ git clone https://github.com/ninashulman/deb_package package_name-1.0
# Cloned package_name-1.0 directory consists of debian\ and DEBIAN\ which were produced by running
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
# Examples of the line to include in the control file: 
#       Architecture: i386
#       Architecture: amd64

# Step 5
# Check that you have usr/, debian/ , DEBIAN/, and README.md , inside package_name-1.0/

# Step 6
# Build a source package package_name_1.0-1.dsc
$ cd package_name-1.0/
$ debuild -S
#   click y for yes when prompted   

# Step 7
# Go outside of_name-1.0/ and observe package_name_1.0-1.dsc being created there 
$ cd ..

# Step 8
# Build a binary debian package package_name_1.0-1_i386.deb in the current directory
$ dpkg-deb -b package_name-1.0 .

# Done! package_name_1.0-1_i386.deb is ready to be used  for installation on Ubuntu machine
# You may rup dpkg -I (with capital I) to see info about this package: $ dpkg -I  package_name_1.0-1_i386.deb

# ####################
# How to install a debian package on Ubuntu machine
# ####################

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

