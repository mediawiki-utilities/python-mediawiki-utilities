from distutils.core import setup

setup(
	name='MW Utilities',
	version='0.0.1',
	author='Aaron Halfaker',
	author_email='aaron.halfaker@gmail.com',
	packages=['mw', 
	          'mw.api', 
	          'mw.database', 
	          'mw.dump', 
	          'mw.lib', 
	          'mw.lib.events', 
	          'mw.lib.reverts', 
	          'mw.lib.sessions', 
	          'mw.lib.title',
	          'mw.scripts',
	          'mw.types',
	          'mw.util'],
	scripts=[],
	url='http://pypi.python.org/pypi/MW_Utilities',
	license='LICENSE',
	description='A set of utilities for working with MediaWiki data.',
	long_description=open('README.rst').read(),
	install_requires=[
	    "argparse >= 1.1",
	    "requests >= 2.0.1"]
)
