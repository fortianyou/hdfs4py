#encoding=utf-8
#########################################################################
# File Name: test.py
# Author: GuoTianyou
# mail: fortianyou@gmail.com
# Created Time: 五  2/24 23:02:37 2017
#########################################################################
import hadoop
import multiprocessing as mp

def func(fs,hf):
   [nbytes, sres ] = hf.read(134217728) 
   print sres
   print fs.setWorkingDirectory("/user/roger")
   print fs.getWorkingDirectory()
   print "Hello world"


fs = hadoop.HadoopDFS("10.141.105.109",9000)
hf = hadoop.HadoopFile(fs, 'hdfs://10.141.105.109:9000/user/classifation/train_23class.txt', is_read=True)
#print fs.getWorkingDirectory()
#print fs.setWorkingDirectory("/user/roger")
#print fs.getWorkingDirectory()
#hf = hadoop.HadoopFile(fs, 'hdfs://10.141.105.109:9000/user/classifation/train_23class.txt', is_read=True)
#[nbytes, sres ] = hf.read(134217728)
process = mp.Process(name="Proc", target = func, args=(fs,hf))
process.start()

