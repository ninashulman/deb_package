import sys
import os
import optparse

packageName = 'stackstorm-capacity'
version = '-1.0'
packageVerName = packageName + version
sourceDir = './usr/share/' + packageName
tmpDir = 'debtmp'
defaultBranch = 'master'

workDir = os.getcwd()
packageDir = workDir + '/' + 'artifacts/debPackages/'
packageFileName = ""

def cleanUp(msg):
    os.chdir(workDir)
    if os.path.exists(tmpDir):
        os.system('rm -rf ' + tmpDir)
    print msg
    sys.exit()

def cloneGithubSource(branch):
    # Clone source into stackstorm-capacity-1.0/usr/share/stackstorm-capacity/
    # os.system returns 0 if the action completed successfully and error code (> 0) if action failed
    if (os.system('git clone https://github.com/StackStorm/osh -b %s' % branch) or
        os.system('git clone https://github.com/StackStorm/osh-data -b %s' % branch) or
        os.system('git clone https://github.com/StackStorm/osh-ui -b %s' % branch)
        ):
        # if os.system returs error code, then if statatemnt is true
        cleanUp('Failed to clone StockStorm source code. Cannot proceed building package.')    


def build(args):
    if os.system('sudo apt-get install devscripts dh-make'):
    	print "Failed to install debian build tools: devscripts and dh-make"
    	print "Failed.  Cannot build without the tools."
    	sys.exit()
   
    # Create a temp directory for build and source files
    if os.path.exists(tmpDir):
        os.system('rm -rf %s' % tmpDir)

    os.makedirs(tmpDir)
    os.chdir(tmpDir)
    
    # Clone the content of https://github.com/ninashulman/deb_package into stackstorm-capacity-1.0/
    if os.system('git clone https://github.com/ninashulman/deb_package %s -b master' % packageVerName):
            cleanUp('Failed to clone debian files. Cannot proceed building package.')

    # Create directory for source code
    os.chdir('./'+ packageVerName)
    os.makedirs(sourceDir)
    print 'Created %s directory for StackStorm source code' % sourceDir
    os.chdir(sourceDir)

    # Get source code from github or specified path
    if "-s"  in args:
        i = args.index("-s")
        src_dir = args[i+1]   
        os.system('cp -rf %s/* .' % src_dir)
    elif "-b" in args:
        i = args.index("-b")
        branch_name = args[i+1]
        cloneGithubSource(branch_name)
    else:   
        # Clone source into stackstorm-capacity-1.0/usr/share/stackstorm-capacity/
        cloneGithubSource(defaultBranch)

    if not "-w" in args:
        # Download and unzip solr
        if (os.system('wget http://mirrors.sonic.net/apache/lucene/solr/4.6.0/solr-4.6.0.tgz') or
            os.system('tar -xvpf solr-4.6.0.tgz') or
            os.system('rm -f solr-4.6.0.tgz')
            ):
            # if os.system returs error code, then if statatemnt is true
            cleanUp('Failed to download and unzip solr used by StackStorm. Discontinue the building process.')
    
    os.chdir('%s/%s/%s' % (workDir, tmpDir, packageVerName))

    if os.path.exists(tmpDir):
        os.chdir(tmpDir)
        os.chdir (packageVerName)

    # Build a source package stackstorm-capacity_1.0-1.dsc
    if os.system('debuild --no-tgz-check -S'):
        # if os.system returs error code, then if statatemnt is true
        cleanUp('Building source package failed')

    # Build a binary debian package
    os.chdir('../')
    if os.system('dpkg-deb -b %s .' % packageVerName):
        # if os.system returs error code, then if statatemnt is true
        cleanUp('Building binary .deb package failed')

    # Store Debian package in the outside directory ../artifacts/debPackages 
    files = os.listdir('.')
    for fileName in files:
        if fileName.endswith(".deb"):
            if os.path.exists(packageDir):
                oldFileNames = os.listdir(packageDir)
                if fileName in oldFileNames:
                    os.system('mv %s%s %s%s-old' % (packageDir, fileName, packageDir, fileName))
                    print 'Previously built %s is renamed into %s-old' % (fileName, fileName)
            else:
                os.makedirs(packageDir)
      
            if os.system('mv %s %s' % (fileName, packageDir)):
                # if os.system returs error code, then if statatemnt is true
                cleanUp('Storing binary .deb package failed')
            
            packageFileName = fileName
            print 'Debian package is created successfully and stored in %s directory' % packageDir

    # Removing build directory'
    os.chdir('../')
    if not "-m" in args:
        os.system('rm -rf ' + tmpDir)

    if "-d" in args:
        os.system('dpkg -I %s%s' % (packageDir, packageFileName))

    if "-p" in args:
        print "Installing all prerequisites documented for this package"
        os.system('git clone https://github.com/dzimine/deploy -b master')
        os.system('./deploy/install-prereqs.sh')
        os.system('rm -rf deploy')

    if "-i" in args:
        print "Installing the package after it is built"
        os.system('sudo dpkg -i %s%s' % (packageDir, packageFileName))   

def usage():
    print
    print "Usage:  python %s [<option> ...]" % os.path.basename(sys.argv[0])
    print
    print "Purpose: Build %s_amd64.deb package for 64 bit Ubuntu." % packageVerName
    print "\t If no additional commands or options are specified, the package is built "
    print "\t from the github master branch source and stored locally in the"
    print "\t %s directory, while all intermediate files are deleted." % packageDir
    print 
    print "Options:"
    print "  -s <src_dir>\t\tBuild package from the source in the specified directory insted of source in github."
    print "  -p  ...\t\tInstall all prerequisites documented for this package."
    print "  -w  ...\t\tDO NOT upload, unzip and include Solr (open source search platform) into this package."
    print "  -b <branch_name>\tClone from the specified branch (master by default)."
    print "  -m  ...\t\tDO NOT clean up all intermediate files collected in %s directory." % tmpDir 
    print "  -d  ...\t\tDisplay package description after it is built."
    print "  -i  ...\t\tInstall package after it is built."
    print "  -h  ...\t\tShow this help message."

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    try:
        if "-h" in argv or "--help" in argv:
            usage()
            sys.exit(2)
        else:
            build(argv)
    except Exception, err:
        print err

if __name__ == "__main__":
    sys.exit(main())

