"""
Python wrapper lib for libhdfs

There are two basic class: HadoopDFS and HadoopFile.

If you have any problem while using it, pls contact to yzcaijunjie@gmail.com

"""

import hdfs4py
import cStringIO
import re


class HadoopDFS:
    """
        Give some methods to connect to HDFS, you can rename,delete,create files/directory etc on HDFS.
    """
    
    def __init__(self,namenode="default",port=0):
        """
            Initial function

            @type namenode: string
            @param namenode: the HDFS namenode you wanted to connect, you can see at hadoop-site.xml. by default, it is assigned to "default"
            @type port: int
            @param port: HDFS port, also can be found in hadoop-site.xml. by default, it is assigned to 0

            for example:
                
            >>> import hadoop
            >>> cluster = hadoop.HadoopDFS("ns-lsp","lsptest","hadoop ugi",64310)
            
        """
        self.hdfs = self.connect(namenode,port)

    def connectAsUser(self,user,namenode,port):
        """
            Connect to a hdfs file system as a specific user

            @type user: string
            @param user: user name for login in 
            @type namenode: string
            @param namenode: The HDFS namenode you wanted to connect, you can see at hadoop-site.xml.
            @type port: int
            @param port: HDFS port, also can be found in hadoop-site.xml. 

            @rtype: hdfsFS
            @return: Returns a handle to the filesystem or NULL on error.
        """
        hdfsFS = hdfs4py.hdfsConnectAsUser(namenode,port,user)
        if hdfsFS == None:
            raise StandardError("Could not connect as %s" % user)
        return hdfsFS

    def connect(self, namenode, port):
        """
            Connect to a hdfs file system

            Forces a new instance to be created
            
            @type namenode: string
            @param namenode: The NameNode.
            @type port: int
            @param port: The port on which the server is listening.

            @rtype: hdfsFs
            @return: Returns a handle to the filesystem or raise error.
        """
        hdfsFS = hdfs4py.hdfsConnect(namenode, port)
        if hdfsFS == None:
            raise StandardError("Counld not connect to %s:%s" %(namenode, str(port)) )
        return hdfsFS
    
    def disconnect(self):
        """
            Disconnect from the hdfs file system.

            @rtype: int
            @return Returns 0 on success, -1 on error.
        """
        result = hdfs4py.hdfsDisconnect(self.hdfs)
        self.hdfs = None
        del self
        return result

    def getCapacity(self):
        """
            Return the raw capacity of the filesystem
            
            @rtype: int
            @return Returns the raw-capacity; -1 on error.

        """
        return hdfs4py.hdfsGetCapacity(self.hdfs)
    
    def getUsed(self):
        """
            Return the total raw size of all files in the filesystem.
            
            @rtype: int
            @return Returns the total-size; -1 on error
        """
        return hdfs4py.hdfsGetUsed(self.hdfs)
        
    def getWorkingDirectory(self,length=255):
        """
            Get the current working directory for the given filesystem.

            @type length: int
            @param length: the length of name of current working directory

            @rtype: string
            @return: Returns name of current working directory, NULL on error.
        """
        pwd = hdfs4py.hdfsGetWorkingDirectory(self.hdfs,length)
        if pwd.startswith("hdfs://"):
            return re.split(":\d+",pwd)[1]
        else:
            return pwd

    def setWorkingDirectory(self,name):
        """
            Set the working directory. All relative paths will be resolved relative to it. 

            @type name: string
            @param name: The path of the new 'cwd'. 

            @rtype: int
            @return: Returns 0 on success, -1 on error. 
        """
        return hdfs4py.hdfsSetWorkingDirectory(self.hdfs,name)
                             
    def createDirectory(self,name):
        """
            Make the given file and all non-existent parents into directories. 

            @type name: string
            @param name: The path of the directory. 

            @rtype: int
            @return: Returns 0 on success, -1 on error. 
        """
        return hdfs4py.hdfsCreateDirectory(self.hdfs,name)
    
    def copy(self,source,target,t_hadoopDFS=None):
        """
            Copy file from one filesystem to another. by default, on local filesystem.

            @type source: string
            @param source: The path of source file. 
            @type target: string
            @param target: The path of destination file. 
            @type t_hadoopDFS:  hdfsFS
            @param t_hadoopDFS: The handle to destination filesystem. 

            @rtype: int
            @return: Returns 0 on success, -1 on error.

        """

     #   if self.pathExists(source)==-1 or self.pathExists(target_t)==0:
     #       return -1
        if t_hadoopDFS==None:
            t_hadoopDFS = self
        if not isinstance(t_hadoopDFS,HadoopDFS):
            raise TypeError("Target DFS must be a HadoopDFS")
        return hdfs4py.hdfsCopy(self.hdfs,source,t_hadoopDFS.hdfs,target)
    
    def move(self,source,target,t_hadoopDFS=None):
        """
            Move file from one filesystem to another. by default, on local filesystem.

            @type source: string
            @param source: The path of source file. 
            @type target: string
            @param target: The path of destination file. 
            @type t_hadoopDFS:  hdfsFS
            @param t_hadoopDFS: The handle to destination filesystem. 
                                                                       
            @rtype: int
            @return: Returns 0 on success, -1 on error.

        """
     #   if self.pathExists(source)==-1:
     #       return -1
        if t_hadoopDFS==None:
            t_hadoopDFS = self
        if not isinstance(t_hadoopDFS,HadoopDFS):
            raise TypeError("Target DFS must be a HadoopDFS")
        return hdfs4py.hdfsMove(self.hdfs,source,t_hadoopDFS.hdfs,target)
                                                                                 
    def delete(self,filename):
        """
            Delete file. 

            @type filename: string
            @param filename: The path of the file. 

            @rtype: int
            @return: Returns 0 on success, -1 on error. 
        """
     #   if self.pathExists(filename)==-1:
     #       return -1
        return hdfs4py.hdfsDelete(self.hdfs,filename)
    
    def rename(self,old,new):
        """
            Rename file. 

            @type old: string
            @param old: The path of the source file. 
            @type new: string
            @param new: The path of the destination file. 

            @rtype: int
            @return: Returns 0 on success, -1 on error.
        """
     #   if self.pathExists(old)==-1 or self.pathExists(new)==0:
     #       return -1
        return hdfs4py.hdfsRename(self.hdfs,old,new)
            
    def listDirectory(self,path):
        """
            Get list of files/directories for a given directory-path. 

            @type path: string
            @param path: The path of the directory. 

            @rtype: list
            @return: Return a list contained all files in given directory on success, or the length of list is zero.
        """
        if self.pathExists(path) == -1 :
            return -1
        return hdfs4py.hdfsListDirectory(self.hdfs,path)
        

    def pathExists(self,path):
        """
            Checks if a given path exsits on the filesystem 

            @type path: string
            @param path: The path to look for 

            @rtype: int
            @return Returns 0 on success, -1 on error. 
        """
        return hdfs4py.hdfsExists(self.hdfs,path)

    def getDefaultBlockSize(self):
        """
            Get the optimum blocksize.  

            @rtype: int
            @return: Returns the blocksize (bytes); -1 on error. 
        """
        return hdfs4py.hdfsGetDefaultBlockSize(self.hdfs)


    def chmod(self,path,mode):
        """
            hdfsChmod, change file mode bits on HDFS
            
            @type path: string
            @param path: the path to the file or directory 
            @type mode: int
            @param mode: the bitmask to set it to

            @rtype: int
            @return: 0 on success else -1 
        """
     #   if self.pathExists(path)==-1:
     #       return -1
        return hdfs4py.hdfsChmod(self.hdfs,path,mode)

    def chown(self,path,owner,group):
        """
            hdfsChown change file owner and group, it must be super user.
            
            @type path: string
            @param path: the path to the file or directory 
            @type owner: string
            @param owner: this is a string in Hadoop land. Set to null or "" if only setting group 
            @type group: string
            @param group: this is a string in Hadoop land. Set to null or "" if only setting user 
                                                            
            @rtype: int
            @return: 0 on success else -1 
        """
     #   if self.pathExists(path)==-1:
     #       return -1
        return hdfs4py.hdfsChown(self.hdfs,path,owner,group)

    def getHosts(self,path,start,length):
        """
            Get hostnames where a particular block (determined by pos & blocksize) of a file is stored. The last element in the array is NULL. Due to replication, a single block could be present on multiple hosts.
            
            @type path: string
            @param path: The path of the file. 
            @type start: int
            @param start: The start of the block. 
            @type length: int
            @param length: The length of the block. 

            @rtype: list
            @return: the hostnames list which stores the block of a file 

            >>> import hadoop
            >>> cluster = hadoop.HadoopDFS("ns-lsp","lsptest","hadoop ugi",64310)
            >>> print cluster.getHosts("/user/ns-lsp/logs/cjj/a",0,1)
            ['xxxxx']

        """
        if self.pathExists(path)==-1:
            return -1
        return hdfs4py.hdfsGetHosts(self.hdfs,path,start,length)

    def getPathInfo(self,path):
        """
            Get information about a path as a (dynamically allocated) single hdfsFileInfo struct. hdfsFreeFileInfo should be called when the pointer is no longer needed. 
                                                                                                                     
            @type path: string
            @param path: The path of the file. 
                                                                                                                     
            @rtype: class 
            @return: Return a hdfsFileInfo class, if path is not exist, return -1
        """
        if self.pathExists(path)==-1:
            return -1
        pathInfo = hdfs4py.hdfsGetPathInfo(self.hdfs,path)
        return pathInfo

    def setReplication(self,path,replication):
        """
            Set the replication of the specified file to the supplied value 

            @type path: string
            @param path: The path of the file. 
            @type replication: int
            @param replication: specify a replication value for a file

            @rtype: int
            @return: Returns 0 on success, -1 on error. 
        """
        if self.pathExists(path)==-1:
            return -1
        return hdfs4py.hdfsSetReplication(self.hdfs,path,replication)
    
class HadoopFile:
    """
        Give some methods to access the file and modfiy it on HDFS    
    """

    def __init__(self,hadoopdfs,filename,is_read=True,buffsize=8*1024,replication=0,blocksize=0):
        if not isinstance(hadoopdfs,HadoopDFS):
            raise TypeError( "First parameter must  be a HadoopDFS")

        if is_read==True:
            mode = hdfs4py.O_RDONLY
        else:
            mode = hdfs4py.O_WRONLY | hdfs4py.O_CREAT
        
        self.filehandle = hdfs4py.hdfsOpenFile(hadoopdfs.hdfs,filename,mode,buffsize,replication,blocksize)
        
        if self.filehandle==None:
            raise IOError("Could not open file")
        self.hdfs = hadoopdfs.hdfs
        
        self._is_read = is_read
        self._buffersize = buffsize

        if self._is_read :
            self._buf = hdfs4py.buffer(buffsize)

    def read(self, buffsize = None):
        """
            Read data from an open file. 

            @param buffsize: The length of the buffer for storing data.
            @return: 
            
            >>> import hadoop
            >>> cluster = hadoop.HadoopDFS("ns-lsp","lsptest","hadoop ugi",64310)
            >>> fh = hadoop.HadoopFile(cluster,'/user/ns-lsp/logs/cjj/a')
            >>> print fh.read()
            
        """
        try:
            if buffsize == None or buffsize == self._buffersize :
                buffsize = self._buffersize
                buf = self._buf
            else:
                buf = hdfs4py.buffer(buffsize)

            nbytes = hdfs4py.hdfsRead(self.hdfs,self.filehandle, buf, buffsize)
        except IOError,e:
            if file_content==None:
                raise

        return [nbytes, hdfs4py.cdata_buffer(buf, nbytes)]

    def close(self):
        """
            Close an open file. 

            @rtype: int
            @return: Returns 0 on success, -1 on error. 
        """
        return hdfs4py.hdfsCloseFile(self.hdfs,self.filehandle)
        
                           
    def readPos(self,pos,len=32*1024):
        """
            Positional read of data from an open file.  
            
            @type pos: int
            @param pos: Position from which to read 
            @type len: int
            @param len: The length of the buffer for storing data. by default, it is assigned to 32KB
                                                                                                 
            @rtype: string
            @return: Returns the data string in tht HDFS file, or raise some Exceptions
            
            >>> import hadoop
            >>> cluster = hadoop.HadoopDFS("ns-lsp","lsptest","hadoop ugi",64310)
            >>> fh = hadoop.HadoopFile(cluster,'/user/ns-lsp/logs/cjj/a')
            >>> print fh.readPos(3) 
            
        """
        
        file_content = ''

        if pos < 0 :
            raise TypeError
        
        try:
            file_content = hdfs4py.hdfsPread(self.hdfs,self.filehandle,pos,len)
        except IOError,e:
            if file_content==None:
                raise
        return file_content

    def write(self,data):
        """
            Write data into an open file. 

            @type data: string
            @param data: The data that wants to write to HDFS file

            @rtype: int
            @return: Returns the number of bytes written, -1 on error. 

            >>> import hadoop
            >>> cluster = hadoop.HadoopDFS("ns-lsp","lsptest","hadoop ugi",64310)
            >>> fh = hadoop.HadoopFile(cluster,'/user/ns-lsp/logs/cjj/a',False)
            >>> fh.write("Hello World")
            >>> fh.close()
            >>> cluster.disconnect()

            B{Be careful}, you must close the file after writing data into file, or the data will not flush into the file(even use flush()).
            
        """
        return hdfs4py.hdfsWrite(self.hdfs,self.filehandle,data)
        

    def flush(self):                                           
        """
            Flush the data. 

            @rtype: int
            @return: Returns the number of bytes written, -1 on error.
        """
        return hdfs4py.hdfsFlush(self.hdfs,self.filehandle)

    def seek(self,offset):
        """
            Seek to given offset in file. This works only for files opened in read-only mode. 

            @type offset: int
            @param offset: Offset into the file to seek into. 

            @rtype: int
            @return: Returns 0 on success, -1 on error. 
            
        """
        if offset>0:
            i = offset    
        else:
            current_position = self.tell()
            i = min(0,current_position-offset)
        ret = hdfs4py.hdfsSeek(self.hdfs,self.filehandle,i)
        if ret<0:
            raise IOError 
                                                                                        
    def tell(self):
        """
            Get the current offset in the file, in bytes. 

            @rtype: int
            @return: Current offset, -1 on error. 
            
        """
        return hdfs4py.hdfsTell(self.hdfs,self.filehandle)

    def available(self):
        """
            Number of bytes that can be read from this input stream without blocking. 

            @rtype: int
            @return: Returns available bytes; -1 on error. 
        """
        return hdfs4py.hdfsAvailable(self.hdfs,self.filehandle)
