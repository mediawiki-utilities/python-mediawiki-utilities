from distutils.core import setup

setup(
	name='MW Utilities',
	version='0.1.0',
	author='Aaron Halfaker',
	author_email='aaron.halfaker@gmail.com',
	packages=['mwutil', 
	          'mwutil.api', 
	          'mwutil.database', 
	          'mwutil.dump', 
	          'mwutil.lib', 
	          'mwutil.lib.persistence', 
	          'mwutil.lib.reverts', 
	          'mwutil.lib.sessions', 
	          'mwutil.types',
	          'mwutil.util',
	          'mwutil.util.iteration'],
	scripts=[],
	url='http://pypi.python.org/pypi/MW_Utilities',
	license='LICENSE',
	description='A set of utilities for working with MediaWiki data.',
	long_description=open('README.rst').read(),
	install_requires=[
	    "argparse >= 1.1",
	    "requests >= 2.0.1"],
	test_suite = 'nose.collector'
)
