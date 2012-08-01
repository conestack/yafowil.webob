Introduction
============

This is the WebOb integration for YAFOWIL.

This package registers a global preprocessor for yafowil. It wraps the any WebOb 
BaseRequest derived request instance.

Special behaviors: 

- All WebOb params - available at WebObs request in a so called ``MultiDict`` - are
  returned in MultiDicts ``mixed`` flavor. This is how Yafowil expects them. 
  IOW: If a query-key exists several times the values are aggregated in a list.
  If a query-key exists one time, the value is returned as string.  
     
- File Uploads provided by WebOb as ``cgi.FieldStorage`` objects are turned into 
  Dicts with the keys:
  
  file
      file-like object to read data from
      
  filename
      submitted name of the upload
      
  mimetype
      type of the upload
      
  headers
      all headers 
      
  original
      keeps the original ``cgi.FieldStorage`` object

Source Code
===========

The sources are in a GIT DVCS with its main branches at
`github <http://github.com/bluedynamics/yafowil.webob`_.

We'd be happy to see many forks and pull-requests to make YAFOWIL even better.


Contributors
============

- Jens W. Klein <jens [at] bluedynamics [dot] com>

- Robert Niederrreiter <rnix [at] squarewave [dot] at>
