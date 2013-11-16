import sys
import os

packageName = 'stackstorm-capacity'
ver = '-1.0'
buildNum = 1
debDirName = packageName + ver
debFileName = debDirName + '.deb'



# Create tmp directory for temprorary files which will be deleted later
if not os.path.exists('tmp'):
	os.makedirs('tmp')
os.chdir('tmp')

# Clone the content of https://github.com/ninashulman/deb_package into stackstorm-capacity-1.0/
if not os.path.exists('stackstorm-capacity-1.0'):
	os.system('git clone https://github.com/ninashulman/deb_package stackstorm-capacity-1.0 -b master')
else:
	print "Remove or rename tmp/stackstorm-capacity-1.0/ in order to proceed with the build process"
	sys.exit()

# Create directory for source code
os.chdir('./stackstorm-capacity-1.0')
source_dir = './usr/share/stackstorm-capacity'
os.makedirs(source_dir)
print 'Source_dir created = %s' % source_dir
os.chdir(source_dir)

# Clone source into stackstorm-capacity-1.0/usr/share/stackstorm-capacity/
os.system('git clone https://github.com/StackStorm/osh -b master')
os.system('git clone https://github.com/StackStorm/osh-data -b master')
os.system('git clone https://github.com/StackStorm/osh-ui -b master')

# Build a source package stackstorm-capacity_1.0-1.dsc
os.chdir('../../../')
res = os.system('debuild --no-tgz-check -S')
#   click y for yes when prompted   
if res != 0:
	print 'Building source package failed'
	sys.exit(1)

# Build a binary debian package in the current directory
os.chdir('../')
res = os.system('dpkg-deb -b ' + debDirName + ' .')
if res != 0:
	print 'Building binary .deb package failed'
	sys.exit(1)

# Storing deb package and cleaning
files = os.listdir('.')
print 'List of generated files: ' + str (files)
for fileName in files:
    if fileName.endswith(".deb"):
        if os.path.exists('../artifacts/debPackages'):
        	oldFileNames = os.listdir('../artifacts/debPackages')
        	if fileName in oldFileNames:
        		os.system('mv ../artifacts/debPackages/' + fileName + ' ../artifacts/debPackages/' + fileName + '-old')
        		print 'Previously built ' + fileName + ' is renamed into ' + fileName + '-old'
        else:
        	os.makedirs('../artifacts/debPackages')  	
        os.system('mv %s ../artifacts/debPackages' % fileName)
print 'Debian package is created successfully and stored in ./artifacts/debPackages directory'

# Removing tmp directory'
print 'Removing tmp directory to clean up'
os.chdir('../')
os.system('rm -rf tmp')


