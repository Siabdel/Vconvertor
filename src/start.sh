#! /usr/bin/python2.6
#
# Python executable to use. 
PYTHON="/usr/bin/python2.7/python"
APPLI="./startConvertor.py"

# Run APPLI on Python interpreter
#rm -f *.pyc
# *** CHEMIN ACCES
#python ./startConvertor.py
echo $PYTHON
$PYTHON  $APPLI  
##python -m trace --count -C D:\data\SusieRebot\launch.py
