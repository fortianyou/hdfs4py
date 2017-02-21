## hdfs4py是什么？
hdfs4py了提供python调用HDFS的接口。

## 与libhdfs的关系
libhdfs是Hadoop官方提供的一套HDFS C++ API。hdfs4py是用swig技术，对libhdfs提供的API进行封装，以支持python对HDFS的调用。

## 为什么用hdfs4py
由于个人项目的需要，调研了如下几款python调用HDFS的方式：

+ 调研了几个开源的HDFS客户端
    - hdfscli: 使用webhdfs，不符合用户使用习惯
    - pydoop：未安装成功
    - hadoopy：没有提供完整的API，项目缺少维护
+ 调研了python调用java api技术
    - JPype：无法正常找到classpath
    - Pyjnius: 需要JDK 1.6， 无法正常找到classpath
+ 调研了python调用C++ api技术
    - 采用swig技术

最终，采用swig封装HDFS C++ API为python API被发现为最为可行的方式。

## 如何获取安装？
+ git clone https://github.com/fortianyou/hdfs4py.git
+ 安装并配置HDFS
+ 安装swig(本文使用2.0.10版本)
+ 执行如下命令，以编译生成hdfs4py： `python setup.py build_ext --inplace`
+ setup.py的内容如下：
+ 
```
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
```

## 运行示例
`python demo.py`

## 致谢
在项目构建过程中，参考了项目[pyhdfs](https://github.com/qiuqiang1985/pyhdfs)。
