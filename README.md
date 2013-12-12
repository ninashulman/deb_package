Usage:  python builddeb.py [<option> ...]

Purpose: Build debian package for 64 bit Ubuntu.
	       If no additional commands or options are specified, the package is built
	       from the github master branch source and stored locally in the
	       ./artifacts/debPackages directory, while all intermediate files are deleted.

Options:

  -s <src_dir>		  Build package from the source in the specified directory insted of source in github.

  -p  ...           Install all prerequisites documented for this package.

  -w  ...           DO NOT upload, unzip and include Solr (open source search platform) into this package.

  -b <branch_name>  Clone from the specified branch (master by default).

  -m  ...		        DO NOT clean up all intermediate files collected in debtmp directory.

  -d  ...		        Display package description after it is built.

  -i  ...		        Install package after it is built.
  
  -h  ...		        Show this help message.
