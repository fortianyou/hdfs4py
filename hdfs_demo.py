from pyhdfs import *

fs = hdfsConnect('default', 0 )
hdfsFile = hdfsOpenFile( fs, '/tmp/testfile.txt', O_WRONLY | O_CREAT, 0, 0, 0 )

buf = 'Hello world'
num_written_bytes = hdfsWrite(fs, hdfsFile, buf )
hdfsFlush(fs, hdfsFile)
hdfsCloseFile(fs, hdfsFile)
