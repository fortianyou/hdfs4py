#encoding=utf-8
#########################################################################
# File Name: setup.py
# Author: GuoTianyou
# mail: fortianyou@gmail.com
# Created Time: 日  1/ 1 17:35:03 2017
#########################################################################
from distutils.core import setup, Extension
import os
HDH=os.environ['HADOOP_HOME']
headers = HDH + '/include'
libs = HDH + '/lib/native'

hdfs4py_module = Extension('_hdfs4py', 
        sources = ['hdfs4py.i'],
        swig_opts=[ '-Wall',  '-DSWIGWORDLENGTH64' ,'-I'+headers, '-I/usr/include'],
        include_dirs=[headers],
        library_dirs=[libs],
        libraries=['hdfs'])

setup( name = 'hdfs4py', 
        version = '0.1', 
        author = 'SWIG',
        description =  """Simple swig example from docs""",
        ext_modules = [hdfs4py_module],
        py_modules = ["hdfs4py"]
        )
