from setuptools import setup, find_packages
import os

version = '1.1.2'
shortdesc = 'WebOb Integration for YAFOWIL'
longdesc = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
longdesc += open(os.path.join(os.path.dirname(__file__), 'HISTORY.rst')).read()
longdesc += open(os.path.join(os.path.dirname(__file__), 'LICENSE.rst')).read()
tests_require = ['interlude']

setup(name='yafowil.webob',
      version=version,
      description=shortdesc,
      long_description=longdesc,
      classifiers=[
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Software Development',
            'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
            'License :: OSI Approved :: BSD License',                        
      ],
      keywords='webob request response html input widgets',
      author='BlueDynamics Alliance',
      author_email='dev@bluedynamics.com',
      url=u'http://pypi.python.org/pypi/yafowil.webob',
      license='Simplified BSD',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['yafowil'],
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'setuptools',
          'WebOb',
          'yafowil>=1.3',
      ],
      entry_points="""
      [yafowil.plugin]
      register = yafowil.webob:register
      """,
)
