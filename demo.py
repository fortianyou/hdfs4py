#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#  Author : vbarter
#  Mail   : yzcaijunjie@gmail.com


"""

"""
import hdfs4py
import hadoop
import math
import gc

__revision__ = '0.1'


if __name__ == "__main__" :
    
    fs = hadoop.HadoopDFS("10.141.105.109",9000)
    print fs.getWorkingDirectory()
    print fs.setWorkingDirectory("/user/roger")
    print fs.getWorkingDirectory()
    print fs.listDirectory("/user/convDSSM/data-00000")
    file = fs.getPathInfo("/user/convDSSM/data-00000")
    print file["mSize"]
    print file["mBlockSize"]
    print math.ceil(float(file["mSize"]) / file["mBlockSize"])
    #server.setReplication("/user/ns-lsp/logs/cjj/a",3)
    #file = server.getPathInfo("/user/ns-lsp/logs/cjj/a")
    #print file.mReplication
    #fs.copy("/user/ns-lsp/logs/cjj","/user/ns-lsp/logs/cjj_new")
    #server.move("/user/ns-lsp/logs/cjj","/user/ns-lsp/logs/log06/")
    #server.delete("/user/ns-lsp/logs/cjj_new")
    #server.rename("/user/ns-lsp/logs/cjj","/user/ns-lsp/logs/cjj1111")
    #open file
    #data = "hello world"
    #hf = hadoop.HadoopFile(fs,'/user/test/pyhdfs_test.txt', is_read=False)
    #hf.write("pyhdfs, hello world")
    #hf.close()
    hf = hadoop.HadoopFile(fs, '/user/classifation/train_23class.txt',  is_read=True)
    [nbytes, sres1 ] = hf.read(64)
    hf.seek(64)
    [nbytes, sres2 ] = hf.read(64)
    sres0 = sres1 + sres2
    print sres0

    hf.seek(0)
    [nbytes, sres ] = hf.read(128)
    print sres

    print str(sres0 == sres)

   #hf.seek(2)
    #print hf.read()[1].strip()

    #print hf.tell()
    #print hf.available()
    #print fs.getDefaultBlockSize()
    #hf.close()
    #print fs.getHosts("/user/test/pyhdfs_test.txt",0,1)
    #print fs.copy("/user/test/pyhdfs_test.txt", "/user/test/pyhdfs_test_cp.txt" )
   # data1 = "Hello\n"
   # data2 = "baidu\n"
   # fs = hadoop.HadoopDFS("username","password","hadoop ugi",54310)
   # fh = hadoop.HadoopFile(fs,'/user/ns-lsp/logs/cjj/a',False)
   # ret = fh.write(data1)
   # fh.close()
   # fh = hadoop.HadoopFile(fs,'/user/ns-lsp/logs/cjj/a',True)  
   # print "start... : ", fh.read()
   # fh.close()
   # fh = hadoop.HadoopFile(fs,'/user/ns-lsp/logs/cjj/a',False)
   # size = fh.tell()
   # fh.seek(size)
   # fh.write(data2)
   # fh.close()
   # fh = hadoop.HadoopFile(fs,'/user/ns-lsp/logs/cjj/a',True)
   # print "end... : ",fh.read()
    #fh.close()
    fs.disconnect()

    gc.collect()












    
    
