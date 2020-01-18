from setuptools import setup

setup(name='httpdummy',
      version='0.1',
      description='A dummy http server that prints requests and responds',
      url='http://github.com/ksofa2/httpdummy',
      license='Apache 2.0',
      packages=['httpdummy'],
      entry_points={
          'console_scripts': ['httpdummy=httpdummy.server:main'],
      },
      zip_safe=False)
