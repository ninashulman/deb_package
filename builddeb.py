import sys
import os

packageName = 'stackstorm-capacity'
version = '-1.0'
packageVerName = packageName + version
sourceDir = './usr/share/' + packageName
debDirName = packageName + version
debFileName = debDirName + '.deb'

workDir = os.getcwd()

def cleanUp(msg):
    os.chdir(workDir)
    if os.path.exists('debtmp'):
        os.system('rm -rf debtmp')
    print msg
    sys.exit()

if os.system('sudo apt-get install devscripts dh-make'):
	print "Failed to install debian build tools: devscripts and dh-make"
	print "Failed.  Cannot build without the tools."
	sys.exit()

# Create debtmp directory for temprorary files which will be deleted later
if os.path.exists('debtmp'):
    os.system('rm -rf debtmp')

os.makedirs('debtmp')
os.chdir('debtmp')

# Clone the content of https://github.com/ninashulman/deb_package into stackstorm-capacity-1.0/
if os.system('git clone https://github.com/ninashulman/deb_package ' + packageVerName + ' -b master'):
        cleanUp('Failed to clone debian files. Cannot proceed building package.')

# Create directory for source code
os.chdir('./'+ packageVerName)
os.makedirs(sourceDir)
print 'Created %s directory for StackStorm source code' % sourceDir
os.chdir(sourceDir)

# Clone source into stackstorm-capacity-1.0/usr/share/stackstorm-capacity/
# os.system returns 0 if the action completed successfully and error code (> 0) if action failed
if (os.system('git clone https://github.com/StackStorm/osh -b master') or
    os.system('git clone https://github.com/StackStorm/osh-data -b master') or
    os.system('git clone https://github.com/StackStorm/osh-ui -b master')
    ):
    # if os.system returs error code, then if statatemnt is true
    cleanUp('Failed to clone StockStorm source code. Cannot proceed building package.')
    

# Build a source package stackstorm-capacity_1.0-1.dsc
os.chdir('../../../')
if os.system('debuild --no-tgz-check -S'):
    # if os.system returs error code, then if statatemnt is true
    cleanUp('Building source package failed')

# Build a binary debian package
os.chdir('../')
if os.system('dpkg-deb -b ' + debDirName + ' .'):
    # if os.system returs error code, then if statatemnt is true
    cleanUp('Building binary .deb package failed')

# Store Debian package in the outside directory ../artifacts/debPackages 
files = os.listdir('.')
# print 'List of generated files: ' + str (files)
for fileName in files:
    if fileName.endswith(".deb"):
        if os.path.exists('../artifacts/debPackages'):
            oldFileNames = os.listdir('../artifacts/debPackages')
            if fileName in oldFileNames:
                os.system('mv ../artifacts/debPackages/' + fileName + ' ../artifacts/debPackages/' + fileName + '-old')
                print 'Previously built ' + fileName + ' is renamed into ' + fileName + '-old'
        else:
            os.makedirs('../artifacts/debPackages')
  
        if os.system('mv %s ../artifacts/debPackages' % fileName):
            # if os.system returs error code, then if statatemnt is true
            cleanUp('Storing binary .deb package failed')
        
        print 'Debian package is created successfully and stored in ./artifacts/debPackages directory'

# Removing debtmp directory'
os.chdir('../')
os.system('rm -rf debtmp')
