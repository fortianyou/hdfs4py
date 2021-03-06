%module hdfs4py

%include "typemap4py.i"
%{
#include "hdfs.h"
%}

%ignore hdfsTruncateFile(hdfsFS fs, const char* path, tOffset newlength);
%include "hdfs4py.h"
%include "stdint.i"

%constant int O_RDONLY = O_RDONLY;
%constant int O_WRONLY = O_WRONLY;
%constant int O_RDWR = O_RDWR;
%constant int O_APPEND = O_APPEND;
%constant int O_CREAT = O_CREAT;
