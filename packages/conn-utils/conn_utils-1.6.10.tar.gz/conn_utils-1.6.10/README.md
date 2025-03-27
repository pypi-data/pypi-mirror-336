## Name
Python Dependency Confusion

## Description
This repo contains an example Python package that can be used to test dependency confusion. It is designed to be a source distribution (rather than built/wheel). The setup.py file is executed on installation of that package. It references an internal source file and in so doing causes the "__init__.py" to execute when loaded. This file contains code that attempts to install the expected package using the URL supplied as part of the "--extra-url-index". It contains DNS based pingbacks that contain the user, hostname, and current step.

## Usage
apt install python-venv  
python3 -m venv venv  
source ./venv/bin/activate  
pip install build  
python3 -m build  
cd dist  
 
## Testing
pip install --extra-index-url https://nexus.int.snowflakecomputing.com/repository/pypi-internal/simple conn_utils-1.6.10.tar.gz  
  
## Cleanup
deactivate  
cd ..  
rm -rf dist  
rm -rf venv  
  
## Author
Ryan Wincey  

