.. image:: https://img.shields.io/pypi/v/yafowil.webob.svg
    :target: https://pypi.python.org/pypi/yafowil.webob
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/yafowil.webob.svg
    :target: https://pypi.python.org/pypi/yafowil.webob
    :alt: Number of PyPI downloads

.. image:: https://travis-ci.org/bluedynamics/yafowil.webob.svg?branch=master
    :target: https://travis-ci.org/bluedynamics/yafowil.webob

.. image:: https://coveralls.io/repos/github/bluedynamics/yafowil.webob/badge.svg?branch=master
    :target: https://coveralls.io/github/bluedynamics/yafowil.webob?branch=master

This is the WebOb integration for YAFOWIL.

This package registers a global preprocessor for yafowil. It wraps the any WebOb 
BaseRequest derived request instance.

Special behaviors: 

All WebOb params - available at WebObs request in a so called ``MultiDict`` - are
returned in MultiDicts ``mixed`` flavor. This is how Yafowil expects them. 
IOW: If a query-key exists several times the values are aggregated in a list.
If a query-key exists one time, the value is returned as string.  
     
File Uploads provided by WebOb as ``cgi.FieldStorage`` objects are turned into 
Dicts with the keys:
  
**file**
    file-like object to read data from
      
**filename**
    submitted name of the upload
      
**mimetype**
    type of the upload
      
**headers**
    all headers 
      
**original**
    keeps the original ``cgi.FieldStorage`` object


For more information about YAFOWIL:

- `Documentation <http://docs.yafowil.info>`_
- `DEMO - see it Live <http://demo.yafowil.info>`_


Source Code
===========

The sources are in a GIT DVCS with its main branches at
`github <http://github.com/conestack/yafowil.webob>`_.

We'd be happy to see many forks and pull-requests to make YAFOWIL even better.


Contributors
============

- Jens W. Klein
- Robert Niederrreiter
