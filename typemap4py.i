%include "carrays.i"
%array_class(unsigned char, buffer);
%include "cdata.i"
%cdata(unsigned char, buffer);

%typemap(in) (const char* path, int *numEntries) {
//typemap
    if (!PyString_Check($input)) {
        PyErr_SetString(PyExc_ValueError, "Expecting a string");
        return NULL;
    }
   
    $1 = (void*) PyString_AsString($input);
    $2 = (int*) malloc( sizeof(int) );
//typemap
}

%typemap(argout) (int *numEntries) {
//typemap
    int length = *$1;
    PyObject *l = PyList_New(length);
    
    Py_XDECREF($result); /* Blow away any previous result */
    int i;
    for(i=0;i<length;i++)
    {
         PyObject *di = PyDict_New();
         PyObject *mName = PyString_FromString(result[i].mName);
         PyDict_SetItemString(di,"mName",mName);
         PyObject *mSize = PyInt_FromLong(result[i].mSize);
         PyDict_SetItemString(di,"mSize",mSize);
         PyObject *mReplication = PyInt_FromLong(result[i].mReplication);
         PyDict_SetItemString(di,"mReplication",mReplication);
         PyObject *mBlockSize = PyInt_FromLong(result[i].mBlockSize);
         PyDict_SetItemString(di,"mBlockSize",mBlockSize);
         PyObject *mOwner = PyString_FromString(result[i].mOwner);
         PyDict_SetItemString(di,"mOwner",mOwner);
         PyObject *mGroup = PyString_FromString(result[i].mGroup);
         PyDict_SetItemString(di,"mGroup",mGroup);
         PyObject *mLastMod = PyInt_FromLong(result[i].mLastMod);
         PyDict_SetItemString(di,"mLastMod",mLastMod);
         PyObject *mLastAccess = PyInt_FromLong(result[i].mLastAccess);
         PyDict_SetItemString(di,"mLastAccess",mLastAccess);
         tObjectKind mKind = result[i].mKind;
         if(mKind=='D')
         {
                        
             PyDict_SetItemString(di,"mKind",PyString_FromString("Directory"));
         }else if(mKind=='F')
         {
             PyDict_SetItemString(di,"mKind",PyString_FromString("File"));
         }
                
         PyList_SetItem(l,i,di);
    }
    $result = l;
    free($1); 
//typemap
}

%typemap(in) ( char  *buffer, size_t bufferSize) {
//typemap
    if (!PyInt_Check($input) ) {
         PyErr_SetString(PyExc_ValueError, "Expecting an integer");
         return NULL;
    }
    $2 = PyInt_AsLong($input);

    if ( PyErr_Occurred() ) {
         PyErr_SetString( PyExc_ValueError, "Expecting positive integer");
         return NULL;
    }

    $1 = (char*) malloc($2*sizeof(char));
//typemap
}

// typemap for an outgoing buffer
%typemap(in) (const void *buffer, tSize length) {
//typemap
    if (!PyString_Check($input)) {
        PyErr_SetString(PyExc_ValueError, "Expecting a string");
        return NULL;
    }
    $1 = (void *) PyString_AsString($input);
    $2 = PyString_Size($input);
//typemap
}
